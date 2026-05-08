import os
import json
import requests
from seleniumbase import SB

# This reads the URLs from your text file
URL_FILE = "urls.txt"
DATA_FILE = "last_state.json"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def get_urls():
    if os.path.exists(URL_FILE):
        with open(URL_FILE, "r") as f:
            # Reads lines, removes spaces, and ignores empty lines
            return [line.strip() for line in f if line.strip()]
    return []

def send_discord(message):
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"content": message})
        except:
            pass

# Load previous state
history = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try: history = json.load(f)
        except: history = {}

NOTES_TO_CHECK = get_urls()
changed_pages = []

if not NOTES_TO_CHECK:
    print("No URLs found in urls.txt!")
else:
    with SB(uc=True, headless=False) as sb:
        for url in NOTES_TO_CHECK:
            try:
                print(f"Checking: {url}")
                sb.uc_open_with_reconnect(url, 7)
                sb.uc_gui_click_captcha() 
                sb.wait_for_element("textarea", timeout=20)
                
                current_text = sb.get_attribute("textarea", "value")
                
                if url in history and history[url] != current_text:
                    changed_pages.append(url)
                
                history[url] = current_text
                print(f"✅ Success")
            except Exception as e:
                print(f"❌ Failed {url}")

    if changed_pages:
        for page in changed_pages:
            send_discord(f"🔔 **Change detected:** {page}")

    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)
