import os
import time
import base64
import csv
import json
import subprocess
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION SETTINGS ---
WATCH_DIR = os.path.expanduser("~/Desktop/trading_screenshots")
LEDGER_PATH = "ledger.csv"
METRICS_SCRIPT = "update_metrics.py"

# Taps into Cursor's active runtime environment key
API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("CURSOR_API_KEY") or "PASTE_YOUR_KEY_HERE"

os.makedirs(WATCH_DIR, exist_ok=True)

def wait_for_file_ready(file_path, timeout=5):
    """Prevents macOS file-lock glitches by waiting until the screenshot is completely written to disk."""
    start_time = time.time()
    last_size = -1
    while time.time() - start_time < timeout:
        try:
            if os.path.exists(file_path):
                current_size = os.path.getsize(file_path)
                if current_size > 0 and current_size == last_size:
                    with open(file_path, 'rb') as f:
                        return True
                last_size = current_size
        except IOError:
            pass
        time.sleep(0.5)
    return False

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def parse_screenshot_with_vision(image_path):
    if not wait_for_file_ready(image_path):
        print(f"⚠️ [BOT 4] File {os.path.basename(image_path)} is incomplete or locked. Skipping.")
        return None

    print(f"\n👁️  [BOT 4] Image locked in. Running optical vision parser on: {os.path.basename(image_path)}...")
    try:
        base64_image = encode_image(image_path)
    except Exception as e:
        print(f"❌ [BOT 4] Image encoding failed: {e}")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "gpt-4o",
        "response_format": { "type": "json_object" },
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": (
                    "Analyze this MEXC trading terminal screenshot. Focus on the 'Order & Trade History' tab or active positions "
                    "panel. Identify the most recent transaction entry. "
                    "Return a JSON object with EXACTLY these keys: "
                    "\"asset\": (string, e.g., 'ETH' or 'DOGE'), "
                    "\"type\": (string, 'LONG', 'SHORT', 'LOSS', or 'RUNNER'), "
                    "\"size\": (float, the filled amount or total position size), "
                    "\"leverage\": (int, e.g., 500 or 252), "
                    "\"entry_price\": (float), "
                    "\"exit_price\": (float, set to 0 if position is still open or running), "
                    "\"net_pnl_usd\": (float, read the precise realized PNL value or unrealized floating value, keep l precision)."
                )
              },
              {
                "type": "image_url",
                "image_url": { "url": f"data:image/jpeg;base64,{base64_image}" }
              }
            ]
          }
        ],
        "max_tokens": 400
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
        raw_json = result['choices'][0]['message']['content']
        return json.loads(raw_json)
    except Exception as e:
        print(f"❌ [BOT 4] Vision model pipeline failed: {e}")
        return None

def process_and_sync(trade_data):
    if not trade_data:
        print("⚠️ [BOT 4] No transaction data extracted. Aborting sync.")
        return
    
    print(f"📊 [BOT 4] Extracted Parameters: {json.dumps(trade_data, indent=2)}")
    
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, 'r') as f:
            rows = list(csv.reader(f))
            last_id = rows[-1][0] if len(rows) > 1 else "000"
            try:
                numeric_part = ''.join(filter(str.isdigit, last_id))
                next_id = f"{int(numeric_part) + 1:03d}"
            except Exception:
                next_id = "010"
    else:
        next_id = "001"

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    status = "RUNNING" if trade_data['type'] == 'RUNNER' or trade_data['exit_price'] == 0 else "COMPLETE"
    
    with open(LEDGER_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            next_id, timestamp, trade_data['asset'], trade_data['type'], 
            trade_data['size'], trade_data['leverage'], trade_data['entry_price'], 
            trade_data['exit_price'], trade_data['net_pnl_usd'], status
        ])
    print(f"✅ [BOT 4] Row {next_id} safely appended to local {LEDGER_PATH}.")

    try:
        print("🔄 [BOT 4] Regenerating performance metrics markdown dashboard...")
        if os.path.exists(METRICS_SCRIPT):
            subprocess.run(["python3", METRICS_SCRIPT], check=True)
        
        print("🚀 [BOT 4] Initiating Git upstream deployment sequence...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"chore(agent): auto-processed screenshot entry for Trade {next_id}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(f"✨ [BOT 4] SUCCESS! Trade {next_id} is live on your public GitHub profile.")
    except Exception as e:
        print(f"⚠️ [BOT 4] Git pipeline sync failed: {e}")

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return
        data = parse_screenshot_with_vision(event.src_path)
        if data:
            process_and_sync(data)

if __name__ == "__main__":
    print("=========================================================")
    print("🤖 [BOT 4] VISION INFRASTRUCTURE SYNC ENGINE IS ONLINE   ")
    print(f"📂 Watch Folder: {WATCH_DIR}")
    print("⚡ Drop any trading screenshot in to update GitHub instantly.")
    print("=========================================================")
    
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
