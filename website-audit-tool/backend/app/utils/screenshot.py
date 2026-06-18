from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import time

SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def capture_screenshot(url: str):

    domain = urlparse(url).netloc.replace(".", "_")
    filename = f"{domain}_{int(time.time())}.png"

    screenshot_path = SCREENSHOT_DIR / filename

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox"
                ]
            )

            page = browser.new_page(
                viewport={"width": 1920, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
            )

            page.goto(
                url,
                wait_until="load",
                timeout=120000
            )
            
            page.wait_for_timeout(5000)

            page.wait_for_timeout(8000)

            page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            browser.close()

        return str(screenshot_path)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Screenshot Error:", str(e))
        return None