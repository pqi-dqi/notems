import os
import time
import random
from playwright.sync_api import sync_playwright

SIGNATURE = "-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("urls.txt not found")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    with sync_playwright() as p:
        # Launches a real Chromium browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Opening {url}...")
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Wait for the text area to settle
                time.sleep(3)

                # Get the value from the textarea (ID is 't')
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ {url} already has Soup.")
                    continue

                print(f"✍️ Re-occupying {url}...")
                
                # Update text and trigger save
                new_text = current_text + "\n" + SIGNATURE
                page.evaluate(f"new_val => {{ document.getElementById('t').value = new_val; }}", new_text)
                
                # Trigger the site's internal save logic
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('input', { bubbles: true }));")
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('change', { bubbles: true }));")
                
                # Wait for save to complete
                time.sleep(4)
                print(f"🚀 Success!")

            except Exception as e:
                print(f"❌ Failed {url}: {e}")
            
            time.sleep(random.uniform(2, 4))

        browser.close()

if __name__ == "__main__":
    monitor()
