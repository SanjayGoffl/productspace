import sys
import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    alert_triggered = False

    def handle_dialog(dialog):
        nonlocal alert_triggered
        print(f"Dialog triggered: {dialog.message}")
        alert_triggered = True
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    page.goto("http://localhost:8080/index.html")

    # The manual entry form is on phase 2.
    # To get there without validation from phase 1, we might need to fill phase 1
    # or just call goTo(2) using page.evaluate()
    page.evaluate("goTo(2)")

    # Fill in the form with XSS payload
    payload = "<img src=x onerror=alert('XSS_SUCCESS')>"

    page.fill("#m-name", payload)
    page.fill("#m-domain", payload)
    page.fill("#m-url", "http://example.com")

    # Click to add manual competitor
    page.click("#btn-add-manual")

    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/before_fix.png")

    browser.close()

    if alert_triggered:
        print("VULNERABILITY CONFIRMED: Alert was triggered.")
        sys.exit(0)
    else:
        print("NO VULNERABILITY FOUND.")
        sys.exit(1)

with sync_playwright() as playwright:
    run(playwright)
