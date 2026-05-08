import os
import json
import requests
from seleniumbase import SB

# Your list of notes
NOTES_TO_CHECK = [
    "https://note.ms/soup",
    "https://note.ms/example1",
]

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATA_FILE = "last_state.json"

def send_discord(message):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": message})

# Load previous content
history = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            history = json.load(f)
        except:
            history = {}

changed = False

# note.ms uses a textarea with id="note"
with SB(uc=True, headless=True) as sb:
    for url in NOTES_TO_CHECK:
        try:
            sb.uc_open_with_reconnect(url, 4)
            # Wait for the textarea to be visible
            sb.wait_for_element("#note", timeout=15)
            
            # Extract content from the textarea
            current_text = sb.get_attribute("#note", "value")
            
            if url in history and history[url] != current_text:
                send_discord(f"🔔 **Change detected!**\nPage: {url}")
                changed = True
            
            history[url] = current_text
            print(f"Successfully checked {url}")
        except Exception as e:
            print(f"Error checking {url}: {e}")

# Always save the file on the first run so Git doesn't crash
with open(DATA_FILE, "w") as f:
    json.dump(history, f)
