from playwright.sync_api import sync_playwright
import time
import os

os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
os.makedirs("/home/jules/verification/videos", exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a new context with video recording enabled
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos/",
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()

        try:
            page.goto("http://localhost:8080/index.html")

            # Type product details
            page.fill("#p-name", "Test Product <script>alert('xss1')</script>")
            page.fill("#p-price", "999")
            page.fill("#p-desc", "Test description")

            # Add a feature chip with malicious input
            page.fill("#p-feat-input", "Feature <img src=x onerror=alert('xss2')>")
            page.keyboard.press("Enter")

            # Wait a moment for chip to render
            page.wait_for_timeout(1000)

            # Screenshot of Phase 1 to verify chip
            page.screenshot(path="/home/jules/verification/screenshots/phase1_chip.png")

            # Click next
            page.click("#btn-p1-next")
            page.wait_for_timeout(1000)

            # Add manual competitor with malicious input
            page.fill("#m-name", "Comp <svg onload=alert('xss3')>")
            page.fill("#m-domain", "comp.com")
            page.click("#btn-add-manual")

            # Wait a moment for grid to update
            page.wait_for_timeout(1000)

            # Screenshot of Phase 2 to verify grid
            page.screenshot(path="/home/jules/verification/screenshots/phase2_grid.png")

            print("Frontend interaction test completed successfully.")

        except Exception as e:
            print(f"Test failed: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    run()
