import os
import time
import random
from playwright.sync_api import sync_playwright

SIGNATURE = "-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("❌ Error: urls.txt not found!")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    print(f"📋 Found {len(urls)} URLs to check.")

    with sync_playwright() as p:
        print("🚀 Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Visiting: {url}")
                # Faster loading strategy: 'commit' means it just waits for the URL to resolve
                page.goto(url, wait_until="commit", timeout=30000)
                
                # Wait specifically for the text box for up to 10 seconds
                print("⏳ Waiting for text box...")
                page.wait_for_selector("#t", timeout=10000)
                
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ Signature found. Skipping.")
                    continue

                print(f"✍️ Writing signature to {url}...")
                new_text = current_text + "\n" + SIGNATURE
                
                # Execute the save
                page.evaluate("([val]) => { const el = document.getElementById('t'); el.value = val; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }", [new_text])
                
                # Short wait to ensure the site's auto-save kicks in
                time.sleep(3)
                print(f"✨ Successfully updated {url}")

            except Exception as e:
                print(f"⚠️ Warning: Could not process {url}. Error: {e}")
            
            # Small random delay to look human
            time.sleep(random.uniform(1, 3))

        print("🏁 All tasks complete. Closing browser.")
        browser.close()

if __name__ == "__main__":
    monitor()
