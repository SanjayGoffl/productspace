from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8080')

    # Fill in product details with an XSS payload
    page.fill('#p-name', 'Test Product')
    page.fill('#p-price', '100')
    page.fill('#p-desc', 'A nice product')

    # Try an XSS payload in the feature input
    xss_payload = '<img src=x onerror=alert(1)>'
    page.fill('#p-feat-input', xss_payload)
    page.press('#p-feat-input', 'Enter')

    # Check if the alert popped up (it shouldn't)
    dialogs = []
    page.on("dialog", lambda dialog: dialogs.append(dialog))

    # Take a screenshot to see if the chip rendered correctly (escaped)
    page.screenshot(path='/home/jules/verification/screenshots/xss_test.png')

    browser.close()
    print(f"Dialogs caught: {len(dialogs)}")
