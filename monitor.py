import os
import time
import random
from playwright.sync_api import sync_playwright

SIGNATURE = "-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("urls.txt not found! Please create it.")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    with sync_playwright() as p:
        # Launching a real browser engine
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Navigating to {url}...")
                # Wait for the network to be quiet
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Give the site's JavaScript time to render the textarea
                time.sleep(5)

                # Fetch the value from the note.ms text box (id='t')
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ {url} already has your signature.")
                    continue

                print(f"✍️ Signature missing. Updating...")
                new_text = current_text + "\n" + SIGNATURE
                
                # Inject text and trigger the site's internal 'save' events
                page.evaluate(f"new_val => {{ document.getElementById('t').value = new_val; }}", new_text)
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('input', { bubbles: true }));")
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('change', { bubbles: true }));")
                
                # Wait for the 'Auto-save' to finish
                time.sleep(5)
                print(f"🚀 Success! {url} updated.")

            except Exception as e:
                print(f"❌ Failed {url}: {e}")
            
            # Human-like delay between pages
            time.sleep(random.uniform(2, 5))

        browser.close()

if __name__ == "__main__":
    monitor()
