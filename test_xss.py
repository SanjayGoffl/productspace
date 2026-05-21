from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        xss_payload_executed = False

        def handle_dialog(dialog):
            nonlocal xss_payload_executed
            print(f"Dialog opened: {dialog.message}")
            xss_payload_executed = True
            dialog.accept()

        page.on("dialog", handle_dialog)

        print("Navigating to local page...")
        page.goto("http://localhost:8080/")

        # Find the feature input and enter XSS payload
        input_sel = "input#p-feat-input"
        page.wait_for_selector(input_sel)
        page.fill(input_sel, "<img src=x onerror=alert(1)>")
        page.press(input_sel, "Enter")

        # Give it a moment to render and trigger any events
        page.wait_for_timeout(1000)

        # Let's also check a quote payload that might escape the attribute
        page.fill(input_sel, "test')\"><img src=x onerror=alert('xss2')>")
        page.press(input_sel, "Enter")

        page.wait_for_timeout(1000)

        if xss_payload_executed:
            print("FAILED: XSS payload executed!")
        else:
            print("SUCCESS: No XSS payload executed.")

        # Let's verify we can still click remove on the chips
        print("Clicking remove on chips to make sure escaping didn't break functionality...")
        close_buttons = page.locator(".chip button")
        count = close_buttons.count()
        print(f"Found {count} chips.")
        for i in range(count):
            close_buttons.nth(0).click() # Click first one repeatedly
            page.wait_for_timeout(200)

        remaining_count = page.locator(".chip button").count()
        print(f"Remaining chips: {remaining_count}")
        if remaining_count == 0:
            print("SUCCESS: Remove feature works correctly with escaped data.")
        else:
            print("FAILED: Couldn't remove all chips.")

        browser.close()

if __name__ == "__main__":
    main()
