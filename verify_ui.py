from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8080/index.html')

        # Verify Product Name label maps to the input
        page.locator('label[for="p-name"]').click()
        assert page.evaluate("document.activeElement.id") == 'p-name', "Product Name label is not mapped properly to its input."

        page.locator('label[for="p-price"]').click()
        assert page.evaluate("document.activeElement.id") == 'p-price', "Target Price label is not mapped properly to its input."

        page.locator('label[for="p-desc"]').click()
        assert page.evaluate("document.activeElement.id") == 'p-desc', "Short Description label is not mapped properly to its input."

        page.locator('label[for="p-feat-input"]').click()
        assert page.evaluate("document.activeElement.id") == 'p-feat-input', "Key Features label is not mapped properly to its input."

        # Go to next phase so m-name is visible
        page.locator('#p-name').fill('A Product')
        page.locator('#p-desc').fill('A Description')
        page.locator('#btn-p1-next').click()

        page.locator('label[for="m-name"]').click(force=True)
        assert page.evaluate("document.activeElement.id") == 'm-name', "Competitor Name label is not mapped properly to its input."

        # Verify chat-fab has an aria-label
        chat_fab = page.locator('#chat-fab')
        assert chat_fab.get_attribute('aria-label') == 'Chat with your history', "chat-fab aria-label is incorrect or missing."

        # Open chat panel to inspect elements within it
        chat_fab.click(force=True)

        # Verify close chat button has an aria-label
        btn_close_chat = page.locator('#btn-close-chat')
        assert btn_close_chat.get_attribute('aria-label') == 'Close chat', "btn-close-chat aria-label is incorrect or missing."

        # Verify send message button has an aria-label
        chat_send = page.locator('#chat-send')
        assert chat_send.get_attribute('aria-label') == 'Send message', "chat-send aria-label is incorrect or missing."

        # Verify chat textarea has an aria-label
        chat_input = page.locator('#chat-input')
        assert chat_input.get_attribute('aria-label') == 'Chat message', "chat-input aria-label is incorrect or missing."

        # Screenshot to show what the chat looks like
        page.screenshot(path='/home/jules/verification/screenshots/chat_panel.png')

        print("Verification completed successfully!")
        browser.close()

if __name__ == '__main__':
    verify()
