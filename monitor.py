import requests
import time
import random
import os

# Configuration
SIGNATURE = "\n-- Soup"
# The message you want to leave if the page is "empty" or needs occupying
NOTE_CONTENT = "这页无聊的页面已经被占领了。" 

def monitor():
    # 1. Load URLs
    if not os.path.exists('urls.txt'):
        print("Error: urls.txt not found!")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    for url in urls:
        try:
            # Step A: Read the page
            response = requests.get(url, headers=headers, timeout=10)
            current_text = response.text

            # Step B: Rate Limit Safety - Random Sleep
            # This makes the 25-page crawl look less like a bot attack
            time.sleep(random.uniform(2.0, 4.0))

            # Step C: Check if "Soup" is already there
            if SIGNATURE in current_text:
                print(f"✅ {url} is already occupied by Soup.")
                continue
            
            # Step D: If not there, update the page
            print(f"⚠️ {url} changed or cleared! Re-occupying...")
            new_data = {"t": current_text + SIGNATURE}
            
            # Note.ms usually accepts POST requests to update content
            requests.post(url, headers=headers, data=new_data, timeout=10)
            
        except Exception as e:
            print(f"❌ Error checking {url}: {e}")

if __name__ == "__main__":
    monitor()
