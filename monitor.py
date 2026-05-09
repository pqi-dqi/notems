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
        # Launch a real browser
        browser = p.chromium.launch(headless=True)
        # Give it a real human-looking profile
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Opening {url}...")
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Give it a second to load the text area content
                time.sleep(2)

                # Use JavaScript to get the content of the textarea (usually 't' on note.ms)
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ {url} already has Soup.")
                    continue

                print(f"✍️ Re-occupying {url}...")
                
                # We update the textarea and trigger the save event
                new_text = current_text + "\n" + SIGNATURE
                page.evaluate(f"new_val => {{ document.getElementById('t').value = new_val; }}", new_text)
                
                # Mimic a 'change' event to trigger the site's auto-save
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('input', { bubbles: true }));")
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('change', { bubbles: true }));")
                
                # Wait for the save to trigger
                time.sleep(3)
                print(f"🚀 Success!")

            except Exception as e:
                print(f"❌ Failed {url}: {e}")
            
            # Random delay between pages
            time.sleep(random.uniform(2, 5))

        browser.close()

if __name__ == "__main__":
    monitor()
