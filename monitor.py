import os
import json
import requests
from seleniumbase import SB

NOTES_TO_CHECK = [
    "https://note.ms/soup",
    "https://note.ms/example1",
]

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATA_FILE = "last_state.json"

def send_discord(message):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": message})

history = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try: history = json.load(f)
        except: history = {}

changed = False

# We use 'headless2' mode which is better at hiding from Cloudflare
with SB(uc=True, headless2=True, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36") as sb:
    for url in NOTES_TO_CHECK:
        try:
            sb.uc_open_with_reconnect(url, 5)
            
            # This handles the "Turnstile" checkbox if it appears
            sb.uc_gui_handle_captcha() 
            
            # Wait longer and try to find the textarea
            sb.wait_for_element("textarea", timeout=20)
            
            # note.ms usually uses the first textarea on the page
            current_text = sb.get_attribute("textarea", "value")
            
            if url in history and history[url] != current_text:
                send_discord(f"🔔 **Change detected!**\nPage: {url}")
                changed = True
            
            history[url] = current_text
            print(f"✅ Successfully checked {url}")
        except Exception as e:
            print(f"❌ Error checking {url}: {e}")

with open(DATA_FILE, "w") as f:
    json.dump(history, f)
