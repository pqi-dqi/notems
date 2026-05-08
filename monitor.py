import os
import json
import requests
from seleniumbase import SB

# Add your notes here or load from a file
NOTES_TO_CHECK = [
    "https://note.ms/soup",
    "https://note.ms/example1",
    # Add your 100+ URLs here
]

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATA_FILE = "last_state.json"

def send_discord(message):
    requests.post(WEBHOOK_URL, json={"content": message})

# Load previous content
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        history = json.load(f)
else:
    history = {}

changed = False

with SB(uc=True, headless=True) as sb:
    for url in NOTES_TO_CHECK:
        try:
            # UC Open handles the Cloudflare challenge
            sb.uc_open_with_reconnect(url, 4)
            sb.sleep(2) # Wait for JS to load the note content
            
            # note.ms content is usually in the #content element
            current_text = sb.get_text("#content")
            
            if url in history and history[url] != current_text:
                send_discord(f"🔔 **Change detected!**\nPage: {url}")
                changed = True
            
            history[url] = current_text
        except Exception as e:
            print(f"Error checking {url}: {e}")

# Save state if changed
if changed:
    with open(DATA_FILE, "w") as f:
        json.dump(history, f)
