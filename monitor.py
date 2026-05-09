import requests
import time
import random
import os

# Configuration
SIGNATURE = "\n-- Soup"
NOTE_CONTENT = "这页无聊的页面已经被占领了。" 

def monitor():
    if not os.path.exists('urls.txt'):
        print("Error: urls.txt not found!")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest' # This tells the server "I am an app request"
    }

    for url in urls:
        try:
            # 1. Get current content
            response = requests.get(url, headers=headers, timeout=10)
            current_text = response.text
            
            time.sleep(random.uniform(1, 2))

            if SIGNATURE in current_text:
                print(f"✅ {url} already has Soup.")
                continue
            
            print(f"⚠️ {url} needs update. Sending payload...")
            
            # 2. Updated Payload Logic
            # Note.ms often takes the content in a field named 't'
            payload = {'t': current_text + SIGNATURE}
            
            # We use data=payload to send it as form-data
            post_resp = requests.post(url, headers=headers, data=payload, timeout=10)
            
            if post_resp.status_code == 200:
                print(f"🚀 Success! Updated {url}")
            else:
                print(f"❌ Failed to update {url}. Status: {post_resp.status_code}")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    monitor()
