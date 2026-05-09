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
        # Launching the browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Opening {url}...")
                # networkidle waits for the page to stop loading data
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Wait for the site's internal scripts to load
                time.sleep(5)

                # Get the current text from the textarea (ID is 't')
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ {url} is already signed.")
                    continue

                print(f"✍️ Signature missing. Re-occupying...")
                
                # We append our signature
                new_text = current_text + "\n" + SIGNATURE
                
                # Inject the new text into the box
                page.evaluate(f"new_val => {{ document.getElementById('t').value = new_val; }}", new_text)
                
                # This part is key: it tricks the site into thinking a human typed something
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('input', { bubbles: true }));")
                page.evaluate("document.getElementById('t').dispatchEvent(new Event('change', { bubbles: true }));")
                
                # Wait for the site's AJAX to finish saving
                time.sleep(5)
                print(f"🚀 Success for {url}")

            except Exception as e:
                print(f"❌ Failed to process {url}: {e}")
            
            # Slow down to avoid being flagged as a spammer
            time.sleep(random.uniform(3, 6))

        browser.close()

if __name__ == "__main__":
    monitor()
