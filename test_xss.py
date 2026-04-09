from playwright.sync_api import sync_playwright

def test_xss_prevention():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file:///app/index.html")

        # Wait for phase 1 to be active
        page.wait_for_selector("#phase-1.active")

        # Inject XSS payload into the "Add Manually" competitor name input
        xss_payload = '<script>alert("XSS")</script>'
        page.fill("#p-feat-input", xss_payload)
        page.keyboard.press("Enter")

        # Verify the feature chip does not contain unescaped script tag
        chip_content = page.inner_html("#feat-chips")
        if "<script>" in chip_content:
             print("FAIL: Feature chip contains unescaped HTML tag")
             exit(1)
        if "&lt;script&gt;" not in chip_content:
             print(f"FAIL: Feature chip does not contain escaped payload, got: {chip_content}")
             exit(1)
        print("PASS: Feature chip correctly escaped HTML")

        # Proceed to phase 2
        page.fill("#p-name", "Test Product")
        page.fill("#p-desc", "Test description")
        page.click("#btn-p1-next")
        page.wait_for_selector("#phase-2.active")

        # Inject XSS payload into competitor name
        page.fill("#m-name", xss_payload)
        page.fill("#m-domain", "example.com")
        page.click("#btn-add-manual")

        comp_grid_content = page.inner_html("#comp-grid")
        if "<script>" in comp_grid_content:
            print("FAIL: Competitor grid contains unescaped HTML tag")
            exit(1)
        if "&lt;script&gt;" not in comp_grid_content:
            print(f"FAIL: Competitor grid does not contain escaped payload, got: {comp_grid_content}")
            exit(1)
        print("PASS: Competitor grid correctly escaped HTML")

        browser.close()

if __name__ == "__main__":
    test_xss_prevention()