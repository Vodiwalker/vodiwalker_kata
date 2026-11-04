
import asyncio
import os
import socket
import uuid as uuid_lib
from datetime import datetime

logger = None  # در start_tcp_relay() از main ست می‌شه

TCP_LISTEN_PORT = int(os.environ.get("TCP_LISTEN_PORT", "6543"))
RELAY_BUF = 256 * 1024

_server = None


async def _parse_vless_tcp_header(chunk: bytes):
    """مثل parse_vless_header در relay_vless.py، با این تفاوت که UUID واقعی رو هم
    از بایت‌های ۱ تا ۱۷ استخراج می‌کنه (چون اینجا خبری از مسیر URL نیست که UUID رو
    مشخص کنه — باید از خود پروتکل VLESS دربیاد)."""
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos = 1
    raw_uuid = chunk[pos:pos + 16]
    uid = str(uuid_lib.UUID(bytes=raw_uuid))
    pos += 16
    addon_len = chunk[pos]
    pos += 1 + addon_len
    command = chunk[pos]
    pos += 1
    port = int.from_bytes(chunk[pos:pos + 2], "big")
    pos += 2
    addr_type = chunk[pos]
    pos += 1
    if addr_type == 1:
        address = ".".join(str(b) for b in chunk[pos:pos + 4])
        pos += 4
    elif addr_type == 2:
        dlen = chunk[pos]
        pos += 1
        address = chunk[pos:pos + dlen].decode("utf-8", errors="ignore")
        pos += dlen
    elif addr_type == 3:
        ab = chunk[pos:pos + 16]
        pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr type: {addr_type}")
    return uid, command, address, port, chunk[pos:]


async def _pipe_client_to_target(client_reader, target_writer, conn_id, uid, check_and_use, throttle):
    try:
        while True:
            data = await client_reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                break
            await throttle(uid, len(data))
            target_writer.write(data)
            if target_writer.transport.get_write_buffer_size() > RELAY_BUF:
                await target_writer.drain()
    except Exception:
        pass
    finally:
        try:
            target_writer.write_eof()
        except Exception:
            pass


async def _pipe_target_to_client(target_reader, client_writer, conn_id, uid, check_and_use, throttle):
    first = True
    try:
        while True:
            data = await target_reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                break
            await throttle(uid, len(data))
            payload = (b"\x00\x00" + data) if first else data
            first = False
            client_writer.write(payload)
            if client_writer.transport.get_write_buffer_size() > RELAY_BUF:
                await client_writer.drain()
    except Exception:
        pass


def _client_ip(writer) -> str:
    try:
        peer = writer.get_extra_info("peername")
        return peer[0] if peer else "نامشخص"
    except Exception:
        return "نامشخص"


async def _handle_client(reader, writer):
    import secrets as _secrets
    from main import (
        LINKS, LINKS_LOCK, stats, hourly_traffic, connections, error_logs,
        is_link_allowed, is_ip_allowed, save_state, log_activity, now_ir,
    )
    from speed_limit import throttle
    from outbound_proxy import open_target_connection

    async def check_and_use(uid: str, n: int) -> bool:
        async with LINKS_LOCK:
            link = LINKS.get(uid)
            if link is None:
                return False
            if not is_link_allowed(link):
                return False
            link["used_bytes"] += n
            stats["total_bytes"] += n
            hourly_traffic[now_ir().strftime("%H:00")] += n
        return True

    conn_id = _secrets.token_urlsafe(6)
    ip = _client_ip(writer)
    target_writer = None
    uid = None

    try:
        first_chunk = await asyncio.wait_for(reader.read(RELAY_BUF), timeout=15.0)
        if not first_chunk:
            return

        uid, command, address, port, payload = await _parse_vless_tcp_header(first_chunk)

        async with LINKS_LOCK:
            link = LINKS.get(uid)

        if not is_link_allowed(link):
            logger and logger.warning(f"🚫 TCP rejected uuid={uid[:8]}… (not allowed)")
            return

        if not is_ip_allowed(link, uid, ip):
            log_activity("connection", f"اتصال TCP {ip} به کانفیگ «{link.get('label','?')}» رد شد (محدودیت IP)", "warn")
            return

        connections[conn_id] = {
            "uuid": uid, "ip": ip, "transport": "vless-tcp",
            "connected_at": datetime.now().isoformat(), "bytes": 0,
        }
        logger and logger.info(f"✅ TCP [{conn_id}] uuid={uid[:8]}… ip={ip} total={len(connections)}")
        log_activity("connection", f"اتصال TCP جدید از {ip} (کانفیگ {link.get('label','?')})", "info")

        if not await check_and_use(uid, len(first_chunk)):
            return
        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += len(first_chunk)

        target_reader, target_writer = await open_target_connection(link, address, port, timeout=10.0)
        sock = target_writer.transport.get_extra_info("socket")
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        if payload:
            target_writer.write(payload)
            await target_writer.drain()

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(_pipe_client_to_target(reader, target_writer, conn_id, uid, check_and_use, throttle)),
                asyncio.create_task(_pipe_target_to_client(target_reader, writer, conn_id, uid, check_and_use, throttle)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state())

    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "tcp connection timeout", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger and logger.error(f"TCP relay error [{conn_id}]: {exc}")
    finally:
        if target_writer:
            try:
                target_writer.close()
                await target_writer.wait_closed()
            except Exception:
                pass
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        connections.pop(conn_id, None)
        logger and logger.info(f"🔌 TCP closed [{conn_id}]")


async def start_tcp_relay(app_logger=None):
    """در startup اصلی main.py صدا زده می‌شه. اگه پورت قابل bind نباشه (مثلاً از قبل
    اشغال شده)، فقط لاگ می‌کنه و کل برنامه رو کرش نمی‌ده."""
    global _server, logger
    logger = app_logger
    try:
        _server = await asyncio.start_server(_handle_client, "0.0.0.0", TCP_LISTEN_PORT)
        logger and logger.info(f"VLESS-TCP relay listening on 0.0.0.0:{TCP_LISTEN_PORT}")
    except Exception as exc:
        logger and logger.warning(f"VLESS-TCP relay could not start on port {TCP_LISTEN_PORT}: {exc}")


async def stop_tcp_relay():
    global _server
    if _server:
        _server.close()
        try:
            await _server.wait_closed()
        except Exception:
            pass
        _server = None
