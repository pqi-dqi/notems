import os
import requests
import json
from seleniumbase import SB

# Configuration
NOTES_TO_WATCH = ["note1", "note2", "note3"] # Add your 100+ names here
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']
DATA_FILE = "last_known_state.json"

def get_note_content(note_name):
    url = f"https://note.ms/{note_name}"
    # The 'uc=True' is the secret sauce for Cloudflare
    with SB(uc=True, headless=True) as sb:
        try:
            sb.uc_open_with_reconnect(url, 5) # 5 sec wait for CF challenge
            # note.ms stores content in a div with id 'content'
            return sb.get_text("#content")
        except Exception as e:
            print(f"Failed to fetch {note_name}: {e}")
            return None

def main():
    # Load previous data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            history = json.load(f)
    else:
        history = {}

    for note in NOTES_TO_WATCH:
        current_text = get_note_content(note)
        if current_text and current_text != history.get(note):
            # Send Discord Notification
            msg = {"content": f"🚨 **Change detected in {note}!**\nhttps://note.ms/{note}"}
            requests.post(DISCORD_WEBHOOK, json=msg)
            history[note] = current_text

    # Save new state
    with open(DATA_FILE, 'w') as f:
        json.dump(history, f)

if __name__ == "__main__":
    main()
