import os
import time
import random
from playwright.sync_api import sync_playwright

SIGNATURE = "-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("urls.txt not found!")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for url in urls:
            try:
                print(f"🌐 Visiting {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Ensure the textarea 't' is actually on the screen
                page.wait_for_selector("#t", timeout=10000)
                
                current_text = page.evaluate("() => document.getElementById('t').value")

                if SIGNATURE in current_text:
                    print(f"✅ Already signed.")
                    continue

                print(f"✍️ Writing signature...")
                new_text = current_text + "\n" + SIGNATURE
                
                # Inject and trigger events
                page.evaluate(f"new_val => {{ 
                    const el = document.getElementById('t');
                    el.value = new_val;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}", new_text)
                
                # Give the AJAX call time to finish
                time.sleep(5)
                print(f"🚀 Success!")

            except Exception as e:
                print(f"❌ Error at {url}: {e}")
            
            time.sleep(random.uniform(2, 4))

        browser.close()

if __name__ == "__main__":
    monitor()
