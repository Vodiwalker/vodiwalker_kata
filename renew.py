import os
import time
from playwright.sync_api import sync_playwright

EMAIL = os.environ.get("KATABUMP_EMAIL")
PASSWORD = os.environ.get("KATABUMP_PASSWORD")
SERVER_ID = os.environ.get("SERVER_ID", "d1712508")

def main():
    if not EMAIL or not PASSWORD:
        print("❌ خطا: متغیرهای KATABUMP_EMAIL یا KATABUMP_PASSWORD در Secrets تعریف نشده‌اند.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        try:
            print("🔄 در حال ورود به صفحه لاگین Katabump...")
            page.goto("https://control.katabump.com/auth/login", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            print("🔑 در حال وارد کردن اطلاعات لاگین...")
            # پیدا کردن فیلد ایمیل/نام‌کاربری با چند سلکتور پشتیبان
            user_input = page.locator('input[name="username"], input[name="email"], input[type="text"], input[type="email"]').first
            pass_input = page.locator('input[name="password"], input[type="password"]').first

            user_input.fill(EMAIL)
            pass_input.fill(PASSWORD)

            # کلیک روی دکمه ورود
            submit_btn = page.locator('button[type="submit"], input[type="submit"]').first
            submit_btn.click()

            page.wait_for_timeout(8000)

            print(f"🌐 در حال هدایت به سرور {SERVER_ID}...")
            page.goto(f"https://control.katabump.com/server/{SERVER_ID}", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            # بررسی و کلیک دکمه Renew
            renew_btn = page.locator('button:has-text("Renew"), a:has-text("Renew")')
            if renew_btn.count() > 0 and renew_btn.first.is_visible():
                renew_btn.first.click()
                print("🎉 دکمه Renew با موفقیت کلیک شد!")
                page.wait_for_timeout(3000)
            else:
                print("ℹ️ دکمه Renew در حال حاضر فعال نیست یا سرور نیازی به تمدید ندارد.")

        except Exception as e:
            print(f"❌ خطایی رخ داد: {e}")
            # ذخیره تصویر از صفحه جهت عیب‌یابی دقیق
            page.screenshot(path="error_screenshot.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    main()
