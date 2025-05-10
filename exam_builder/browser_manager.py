# ----- exam_builder/browser_manager.py -----
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import subprocess, sys, time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def launch_debug_browser(browser_url: str = "http://127.0.0.1:9222") -> None:
    """Start Chrome in remote-debugging mode."""
    print("Launching Chrome in debug mode...")
    if sys.platform.startswith('win'):
        chrome_cmd = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        profile = r"C:\Temp\chrome-debug-profile"
    elif sys.platform.startswith('darwin'):
        chrome_cmd = "open -a 'Google Chrome' --args"
        profile = "/tmp/chrome-debug-profile"
    else:
        chrome_cmd = "google-chrome"
        profile = "/tmp/chrome-debug-profile"

    args = [
        chrome_cmd,
        "--remote-debugging-port=9222",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
        "about:blank"
    ]
    try:
        subprocess.Popen(args)
    except Exception as e:
        print(f"Error launching Chrome: {e}")


def wait_for_debug_port(url: str = "http://127.0.0.1:9222/json/version", timeout: int = 20, interval: float = 0.5) -> None:
    """Poll Chrome's debug port until available or timeout."""
    print("Waiting for Chrome debug port to become available...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urlopen(url) as response:
                if response.status == 200:
                    print("Chrome debug port is available.")
                    return
        except (HTTPError, URLError):
            pass
        time.sleep(interval)
    raise Exception("Chrome debug port did not become available in time.")


def setup_browser(browser_url: str = "http://127.0.0.1:9222") -> Page:
    """Connect or launch Chrome debug, navigate to exam.net, and return a ready Playwright Page."""
    playwright = sync_playwright().start()
    try:
        browser = playwright.chromium.connect_over_cdp(browser_url)
    except Exception:
        launch_debug_browser(browser_url)
        wait_for_debug_port()
        browser = playwright.chromium.connect_over_cdp(browser_url)

    contexts = browser.contexts
    context = contexts[0] if contexts else browser.new_context()
    page = context.pages[0] if context.pages else context.new_page()

    # Navigate if not already on exam.net with 'Create question'
    try:
        if "exam.net" not in page.url or page.locator('button:has-text("Create question")').count() == 0:
            page.goto("https://exam.net")
            print("Navigated to exam.net. Please log in and open the desired exam.")
            input("Press ENTER after login/setup...")
        else:
            print("Using existing exam.net debug page.")
    except Exception as e:
        print(f"Error during navigation setup: {e}")
        page.goto("https://exam.net")
        input("Press ENTER after login/setup...")

    return page