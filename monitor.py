import cloudscraper
import time
import random
import os

SIGNATURE = "\n-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("Error: urls.txt missing")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    # Create a scraper that bypasses Cloudflare/Bot protection
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    for url in urls:
        try:
            # 1. Get current content
            print(f"👀 Checking {url}...")
            resp = scraper.get(url, timeout=15)
            
            if resp.status_code != 200:
                print(f"❌ Could not reach {url}. Status: {resp.status_code}")
                continue

            current_text = resp.text

            # If our signature is there, we are good
            if SIGNATURE in current_text:
                print(f"✅ Already occupied.")
                continue
            
            # Anti-detection delay
            time.sleep(random.uniform(4, 7))
            
            # 2. Update the page
            print(f"✍️ Re-occupying...")
            payload = {'t': current_text + SIGNATURE}
            
            # Some sites prefer the data sent as a string or form
            post_resp = scraper.post(
                url, 
                data=payload, 
                headers={'X-Requested-With': 'XMLHttpRequest', 'Referer': url},
                timeout=15
            )
            
            if post_resp.status_code == 200:
                print(f"🚀 SUCCESS! Soup signature added.")
            else:
                print(f"❌ Failed. Status: {post_resp.status_code}")

        except Exception as e:
            print(f"❌ Script Error: {e}")

if __name__ == "__main__":
    monitor()
