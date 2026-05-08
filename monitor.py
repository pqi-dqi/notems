import os
import json
import requests
from seleniumbase import SB

# 1. ADD YOUR URLS HERE
NOTES_TO_CHECK = [
    "https://note.ms/soup",
    "https://note.ms/example1",
]

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
DATA_FILE = "last_state.json"

def send_discord(message):
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"content": message})
        except Exception as e:
            print(f"Webhook failed: {e}")

# Load previous state
history = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            history = json.load(f)
        except:
            history = {}

changed_pages = []

# Removed slow_mode from here to fix the TypeError
with SB(uc=True, headless=False) as sb:
    for url in NOTES_TO_CHECK:
        try:
            print(f"Checking: {url}")
            # Step 1: Open the page
            sb.uc_open_with_reconnect(url, 7)
            
            # Step 2: Bypass Cloudflare Checkbox
            sb.uc_gui_click_captcha() 
            
            # Step 3: Wait for the textarea
            # Using a more generic selector in case the ID is slightly different
            sb.wait_for_element("textarea", timeout=25)
            
            # Step 4: Get text (note.ms puts content in the 'value' of the textarea)
            current_text = sb.get_attribute("textarea", "value")
            
            # Step 5: Compare
            if url in history and history[url] != current_text:
                changed_pages.append(url)
            
            history[url] = current_text
            print(f"✅ Success")
            
        except Exception as e:
            print(f"❌ Failed {url}: {str(e)[:50]}...")

# Send notifications if there are changes
if changed_pages:
    for page in changed_pages:
        send_discord(f"🔔 **Change detected at:** {page}")

# Save the new state
with open(DATA_FILE, "w") as f:
    json.dump(history, f, indent=4)
