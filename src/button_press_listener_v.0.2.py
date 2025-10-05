import os
import json
import time
import tkinter as tk
from pynput import mouse, keyboard
import sys

# 🔹 Setup AppData config directory
CONFIG_DIR = os.path.join(os.environ["APPDATA"], "MacroTool")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(CONFIG_DIR, "mouse_buttons.json")

# 🔹 Load existing config
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"mouse_buttons": []}
    return {"mouse_buttons": []}

# 🔹 Save config
def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# 🔹 Add mouse button
def add_mouse_button(data, name, value):
    for entry in data.get("mouse_buttons", []):
        if entry["value"] == value:
            return data, False
    data.setdefault("mouse_buttons", []).append({"name": name, "value": value})
    save_config(data)
    return data, True

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("Komisz_01's Input Listener")
root.geometry("550x350")
text = tk.Text(root, bg="black", fg="white", font=("Consolas", 12))
text.pack(fill="both", expand=True)

messages = []
config = load_config()

def log(msg, status=False):
    """Display a message in the GUI log."""
    global messages
    timestamp = time.strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    messages.insert(0, entry)
    messages = messages[:14]  # Keep last 14 messages visible
    text.delete("1.0", tk.END)
    for m in messages:
        if "✅" in m or status:
            text.insert(tk.END, m + "\n", "status")
        else:
            text.insert(tk.END, m + "\n")
    text.tag_config("status", foreground="lime")

# --- Keyboard listener ---
def on_key_press(key):
    try:
        key_name = key.char if hasattr(key, "char") and key.char else str(key)
    except:
        key_name = str(key)

    if key_name.lower() in ("<esc>", "esc", "key.esc"):
        log("🚪 ESC pressed → Exiting listener...")
        root.quit()
        sys.exit(0)

    log(f"🔤 Key pressed: {key_name}")
    return True

# --- Mouse listener ---
def on_click(x, y, button, pressed):
    if pressed:
        btn_name = str(button).replace("Button.", "").upper()

        # Normalize extra buttons
        name_map = {
            "X1": "MB4",
            "X2": "MB5",
            "X3": "MB6",
            "X4": "MB7",
            "X5": "MB8"
        }
        btn_name = name_map.get(btn_name, btn_name)

        msg = f"🖱️ Mouse {btn_name} at ({x},{y})"
        log(msg)
        global config
        config, saved = add_mouse_button(config, f"Mouse {btn_name}", btn_name)
        if saved:
            log(f"✅ Saved Mouse {btn_name} to config", status=True)

# --- Startup display ---
log("🎯 Listening for input... (press ESC to quit)")
if config.get("mouse_buttons"):
    log("💾 Loaded saved mouse buttons:")
    for btn in config["mouse_buttons"]:
        log(f"   • {btn['name']} ({btn['value']})")

# --- Start listeners ---
kb_listener = keyboard.Listener(on_press=on_key_press)
ms_listener = mouse.Listener(on_click=on_click)

kb_listener.start()
ms_listener.start()

# --- Run Tkinter loop ---
root.mainloop()
