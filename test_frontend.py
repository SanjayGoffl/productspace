from playwright.sync_api import sync_playwright
import os
import time

def test_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("file:///app/index.html")

        # We need to simulate XSS vectors to ensure they are escaped
        page.evaluate("""
            state.competitors = [
                { name: "<img src=x onerror=alert(1)>Name", domain: "<script>alert(1)</script>domain.com", price: "99<script>alert(2)</script>", selected: true }
            ];
            renderCompetitorGrid();

            // Set history for testing Drawer and Chat Context List
            localStorage.setItem('ps_history', JSON.stringify([
                {
                    id: '123"><script>alert(1)</script>',
                    timestamp: new Date().toISOString(),
                    product: { name: 'Prod<script>alert(1)</script>', price: '100<script>alert(2)</script>', desc: '', features: [] },
                    competitors: [],
                    analysisData: {}
                }
            ]));
        """)

        # open drawer
        page.evaluate("openDrawer()")
        time.sleep(1)

        # Check if renderCompetitorGrid properly escaped
        comp_card = page.locator(".comp-card").first
        if comp_card.count() > 0:
            print("Competitor HTML:", comp_card.inner_html())
        else:
            print("No Competitor HTML found")

        # Check if renderHistoryDrawer properly escaped
        print("history-list innerHTML:\n", page.locator("#history-list").inner_html())

        page.evaluate("closeDrawer()")
        page.evaluate("openChat()")
        time.sleep(1)

        # Check if renderChatCtxList properly escaped
        print("ctx-list innerHTML:\n", page.locator("#ctx-list").inner_html())

        os.makedirs('/home/jules/verification/screenshots', exist_ok=True)
        page.screenshot(path='/home/jules/verification/screenshots/frontend_verification.png')

        browser.close()

if __name__ == "__main__":
    test_frontend()
