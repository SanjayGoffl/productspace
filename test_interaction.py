from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:8080/index.html')

    # Check for any console errors during load
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)

    # Add a product feature to trigger renderChips() and check for errors
    page.fill('#p-feat-input', 'Feature 1')
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)

    if len(errors) > 0:
        print(f"Found {len(errors)} console errors:")
        for e in errors:
            print(f"- {e}")
    else:
        print("No console errors found after interaction!")

    browser.close()
