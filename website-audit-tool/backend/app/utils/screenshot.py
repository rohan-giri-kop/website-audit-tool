from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import time


# ==========================================================
# SCREENSHOT CONFIGURATION
# ==========================================================

SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

SCREENSHOT_TIMEOUT = 15000

# Small stabilization delay.
# We do NOT wait 13 seconds anymore.
SCREENSHOT_STABILIZE_MS = 1000


# ==========================================================
# SCREENSHOT
# ==========================================================

def capture_screenshot(url: str):

    started_at = time.perf_counter()

    domain = (
        urlparse(url)
        .netloc
        .replace(".", "_")
        .replace(":", "_")
    )

    filename = (
        f"{domain}_{int(time.time())}.png"
    )

    screenshot_path = (
        SCREENSHOT_DIR / filename
    )

    print(
        f"[SCREENSHOT] Starting: {url}"
    )

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-extensions",
                ]
            )

            page = browser.new_page(
                viewport={
                    "width": 1920,
                    "height": 900
                },

                user_agent=(
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/137.0 Safari/537.36"
                )
            )

            # --------------------------------------------------
            # PAGE TIMEOUTS
            # --------------------------------------------------

            page.set_default_navigation_timeout(
                SCREENSHOT_TIMEOUT
            )

            page.set_default_timeout(
                5000
            )

            # --------------------------------------------------
            # LOAD WEBSITE
            # --------------------------------------------------

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=SCREENSHOT_TIMEOUT
            )

            # --------------------------------------------------
            # SHORT STABILIZATION
            # --------------------------------------------------
            #
            # Previously:
            #
            # 5000 ms
            # +
            # 8000 ms
            # =
            # 13000 ms
            #
            # Now:
            #
            # 1000 ms
            #
            # Lighthouse remains responsible for the detailed
            # performance/browser analysis.
            # --------------------------------------------------

            page.wait_for_timeout(
                SCREENSHOT_STABILIZE_MS
            )

            # --------------------------------------------------
            # SCREENSHOT
            # --------------------------------------------------

            page.screenshot(
                path=str(
                    screenshot_path
                ),
                full_page=True,
                animations="disabled"
            )

            browser.close()

        elapsed = (
            time.perf_counter()
            - started_at
        )

        print(
            f"[SCREENSHOT] Complete: "
            f"{elapsed:.2f}s"
        )

        return (
            f"/reports/screenshots/"
            f"{filename}"
        )

    except Exception as e:

        elapsed = (
            time.perf_counter()
            - started_at
        )

        print(
            f"[SCREENSHOT] Failed after "
            f"{elapsed:.2f}s: {e}"
        )

        return None