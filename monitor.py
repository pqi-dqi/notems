import requests
import os
import time
import random

SIGNATURE = "-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        print("❌ urls.txt not found!")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    # Use a real-looking session
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    })

    for url in urls:
        try:
            # 1. Try to get the current content
            print(f"🌐 Checking {url}...")
            # Note.ms often stores content in a way that's hard to GET directly via requests, 
            # so we will try to 'append' by assuming the site handles partial updates or 
            # just sending our signature if we can't read it.
            
            # 2. Send the update
            # Note.ms typically uses a POST to the path with 't' as the key
            topic = url.split('/')[-1]
            post_data = {'t': f"\n{SIGNATURE}"} 
            
            # Some versions of note.ms use a different endpoint, 
            # but usually, it's just a POST to the URL itself.
            response = session.post(url, data=post_data, timeout=10)

            if response.status_code == 200:
                print(f"✅ Posted to {url}")
            else:
                print(f"⚠️ Server returned {response.status_code} for {url}")

        except Exception as e:
            print(f"❌ Error at {url}: {e}")
        
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    monitor()
