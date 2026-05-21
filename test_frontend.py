from playwright.sync_api import sync_playwright
import os

os.makedirs('/home/jules/verification/screenshots', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:8080')
    page.wait_for_selector('#p-name')

    # Enter some malicious inputs to see if they get rendered as text instead of HTML execution
    page.fill('#p-name', '<img src=x onerror=alert(1)>')
    page.fill('#p-price', '999')
    page.fill('#p-desc', 'Desc')
    page.fill('#p-feat-input', 'Feature <script>alert("xss")</script>')
    page.keyboard.press('Enter')

    # Take screenshot of phase 1
    page.screenshot(path='/home/jules/verification/screenshots/phase1.png')

    page.click('#btn-p1-next')

    # Take screenshot of phase 2
    page.wait_for_selector('#m-name')
    page.fill('#m-name', 'Comp <script>alert("xss")</script>')
    page.fill('#m-domain', 'example.com')
    page.click('#btn-add-manual')

    page.wait_for_timeout(500)
    page.screenshot(path='/home/jules/verification/screenshots/phase2.png')

    # Let's interact with chat too
    page.click('#chat-fab')
    page.wait_for_selector('#chat-input')
    page.fill('#chat-input', 'Chat message <script>alert("xss")</script>')
    page.click('#chat-send')
    page.wait_for_timeout(500)
    page.screenshot(path='/home/jules/verification/screenshots/chat.png')

    browser.close()
    print('Testing complete.')
