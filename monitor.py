import requests
import time
import random
import os

SIGNATURE = "\n-- Soup"

def monitor():
    if not os.path.exists('urls.txt'):
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    # Create a session to handle cookies automatically
    session = requests.Session()
    
    # Very specific headers to look like a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://note.ms',
        'Connection': 'keep-alive',
    })

    for url in urls:
        try:
            # 1. 'GET' the page first to look like a visitor and get cookies
            print(f"👀 Visiting {url}...")
            get_resp = session.get(url, timeout=10)
            current_text = get_resp.text
            
            # Anti-detection sleep
            time.sleep(random.uniform(3, 6))

            if SIGNATURE in current_text:
                print(f"✅ {url} is safe.")
                continue
            
            # 2. Prepare the POST with a Referer
            print(f"✍️ Re-occupying {url}...")
            post_headers = {
                'Referer': url,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            payload = {'t': current_text + SIGNATURE}
            
            # Note.ms often uses a simple post, but we'll try to mimic the form
            post_resp = session.post(url, data=payload, headers=post_headers, timeout=10)
            
            if post_resp.status_code == 200:
                print(f"🚀 Success!")
            else:
                print(f"❌ Still getting {post_resp.status_code}. They are blocking the IP.")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    monitor()
