from playwright.sync_api import sync_playwright

def test_xss_manual_competitor():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8080")

        dialogs = []
        page.on("dialog", lambda dialog: dialogs.append(dialog.message) or dialog.dismiss())

        page.fill("#p-name", "Test Product")
        page.fill("#p-price", "100")
        page.fill("#p-desc", "Test Description")

        # Click Next and handle any potential dialog
        page.click("#btn-p1-next")

        page.wait_for_selector("#phase-2.active")

        # Let's wait for auto discovery to finish or fail
        # by waiting for the spinner to disappear or status to change
        page.wait_for_timeout(3000)

        xss_payload = "<img src=x onerror=alert(1)>"
        page.fill("#m-name", xss_payload)
        page.fill("#m-domain", "malicious.com")
        page.click("#btn-add-manual")

        page.wait_for_timeout(2000)

        # Wait for the specific competitor we just added.
        page.wait_for_selector(".comp-name")
        comp_names = page.locator(".comp-name").all_text_contents()

        found = False
        for text in comp_names:
            if "<img src=x onerror=alert(1)>" in text:
                found = True
                break

        assert found, f"Escaped text not found in competitor list: {comp_names}"
        assert len(dialogs) == 0, f"XSS payload executed! Captured dialogs: {dialogs}"

        browser.close()

if __name__ == "__main__":
    test_xss_manual_competitor()
    print("XSS tests passed!")