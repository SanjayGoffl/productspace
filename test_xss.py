import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(record_video_dir="/home/jules/verification/videos")
    page.goto("http://localhost:8080/index.html")

    # Add a feature that contains XSS attempt
    page.fill("#p-feat-input", "NormalFeature")
    page.press("#p-feat-input", "Enter")

    page.fill("#p-feat-input", "XSS<img src=x onerror=alert(1)>")
    page.press("#p-feat-input", "Enter")

    # Check if the text is properly escaped
    html = page.inner_html("#feat-chips")
    print(html)

    # Try to click the remove button of the escaped feature
    # We locate the button inside the chip that has the text 'XSS...'
    time.sleep(1)
    page.screenshot(path="/home/jules/verification/screenshots/chips.png")

    browser.close()
