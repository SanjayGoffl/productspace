from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:8080/index.html')

    # Check for any console errors during load
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)

    title = page.title()
    print(f"Page title: {title}")

    if len(errors) > 0:
        print(f"Found {len(errors)} console errors:")
        for e in errors:
            print(f"- {e}")
    else:
        print("No console errors found!")

    browser.close()
