import os
import time
import random
from playwright.sync_api import sync_playwright

SIGNATURE = "-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("❌ urls.txt not found!")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    with sync_playwright() as p:
        # 1. Use a more convincing User Agent and standard window size
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        
        # 2. Add extra stealth: mask webdriver property
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        for url in urls:
            try:
                print(f"🌐 Visiting {url}")
                # Increased timeout and changed wait strategy
                response = page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Check if we got blocked (403 Forbidden)
                if response.status == 403:
                    print(f"🚫 Blocked by site (403) at {url}")
                    continue

                # 3. Use a more flexible selector check
                print("⏳ Waiting for content...")
                page.wait_for_selector("#t", timeout=20000)
                
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ Already signed.")
                    continue

                print(f"✍️ Writing signature...")
                new_text = current_text + "\n" + SIGNATURE
                
                # Use 'fill' instead of raw JS injection to mimic typing
                page.fill("#t", new_text)
                
                # Wait for auto-save
                time.sleep(4)
                print(f"🚀 Success!")

            except Exception as e:
                print(f"⚠️ Failed at {url}: {str(e)[:50]}...")
            
            # 4. Longer, more variable sleep to avoid rate-limiting
            time.sleep(random.uniform(3, 7))

        browser.close()

if __name__ == "__main__":
    monitor()
