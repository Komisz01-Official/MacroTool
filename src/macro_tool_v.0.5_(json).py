import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
import keyboard
import json
import os

running = False
rows = []

# --- Load mouse buttons from JSON ---
def load_mouse_buttons():
    try:
        config_dir = os.path.join(os.getenv("APPDATA"), "MacroTool")
        config_path = os.path.join(config_dir, "mouse_buttons.json")

        os.makedirs(config_dir, exist_ok=True)

        # Default friendly list (display_name, internal_value)
        default_buttons = [
            ("Left Click", "MB1"),
            ("Right Click", "MB2"),
            ("Middle Click", "MB3"),
            ("Scroll Up", "MB4"),
            ("Scroll Down", "MB5"),
            ("Side Button 1", "MB6"),
            ("Side Button 2", "MB7"),
            ("Side Button 3", "MB8"),
        ]

        # If file doesn't exist -> create a default JSON
        if not os.path.exists(config_path):
            default_payload = {"mouse_buttons": [{"name": n, "value": v} for n, v in default_buttons]}
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_payload, f, indent=4)
            return default_buttons

        # Load the JSON
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1) Old list format
        if isinstance(data, dict) and "mouse_buttons" in data and isinstance(data["mouse_buttons"], list):
            result = []
            for item in data["mouse_buttons"]:
                name = item.get("name") or f"Mouse {item.get('value')}"
                value = item.get("value")
                result.append((str(name), str(value)))
            if result:
                return result

        # 2) Dict format (button-name: details)
        if isinstance(data, dict):
            result = []
            for k, v in data.items():
                if k.lower() in ("last_key", "last_mouse", "last_joystick", "macros"):
                    continue
                kl = k.lower()
                if (kl.startswith("mb") or "button" in kl or isinstance(v, dict)):
                    display = k.upper() if len(k) <= 5 else k
                    display = f"Mouse {display}"
                    result.append((display, str(k)))
            if result:
                return result

        # 3) Fallback
        return default_buttons

    except Exception as e:
        print("Error loading mouse buttons:", e)
        return []

# ✅ Call the loader here — this defines the variable before all_keys
mouse_buttons_list = load_mouse_buttons()
mouse_buttons = [n for n, v in mouse_buttons_list]

# --- Keyboard keys ---
keyboard_keys = [chr(i) for i in range(97, 123)]  # a-z
keyboard_keys += [str(i) for i in range(0, 10)]   # 0-9
keyboard_keys += [f"F{i}" for i in range(1, 25)]  # F1-F24
keyboard_keys += ["shift", "ctrl", "alt", "tab", "space", "enter", "esc", "backspace"]

# Combine both
all_keys = keyboard_keys + mouse_buttons

# --- GUI ---
root = tk.Tk()
root.title("Komisz_01's Macro Tool with Auto-Loaded Mouse Buttons")

trigger_key = tk.StringVar()

# --- Functions ---
def start_macro():
    global running
    if running or not trigger_key.get():
        return
    running = True
    threading.Thread(target=macro_listener, daemon=True).start()

def stop_macro():
    global running
    running = False
    try:
        if hasattr(keyboard, "unhook_all_hotkeys"):
            keyboard.unhook_all_hotkeys()
    except Exception as e:
        print(f"[⚠] Could not unhook hotkeys safely: {e}")

def macro_listener():
    from pynput import mouse

    trig = trigger_key.get()
    print(f"[ℹ] Listening for trigger: {trig}")

    # 🧠 Detect whether trigger is mouse or keyboard
    is_mouse_trigger = trig.startswith("Mouse") or trig.upper().startswith("MB")

    if is_mouse_trigger:
        # Map the human-readable mouse button name to pynput button
        from pynput.mouse import Button

        button_map = {
            "Mouse Left": Button.left,
            "Mouse Right": Button.right,
            "Mouse Middle": Button.middle,
            "Mouse MB4": Button.x1,
            "Mouse MB5": Button.x2,
            "Mouse MB6": Button.x1,  # fallback for extra buttons
            "Mouse MB7": Button.x2,
            "Mouse MB8": Button.x2
        }

        target_button = button_map.get(trig, Button.left)

        def on_click(x, y, button, pressed):
            if pressed and button == target_button and running:
                print(f"[🖱️] Triggered by {trig} at ({x}, {y})")
                run_sequence()

        with mouse.Listener(on_click=on_click) as listener:
            while running:
                time.sleep(0.1)
            listener.stop()

    else:
        # Keyboard trigger
        try:
            keyboard.add_hotkey(trig, run_sequence)
            print(f"[⌨️] Listening for keyboard trigger: {trig}")
        except Exception as e:
            print(f"[⚠] Failed to bind trigger '{trig}': {e}")
            stop_macro()
            return

        while running:
            time.sleep(0.1)

def run_sequence():
    if not running:
        return
    for key_combo, delay_entry in rows:
        key = key_combo.get()
        try:
            delay = float(delay_entry.get())
        except ValueError:
            delay = 0.1
        if key:
            keyboard.press_and_release(key)
        time.sleep(delay)

def add_row(key_val="", delay_val="0.1"):
    row_num = len(rows) + 1

    key_combo = ttk.Combobox(frame, values=all_keys, state="readonly", width=20)
    key_combo.grid(row=row_num, column=0, padx=5, pady=2)
    if key_val in all_keys:
        key_combo.set(key_val)
    else:
        key_combo.current(0)

    delay_entry = ttk.Entry(frame, width=10)
    delay_entry.insert(0, delay_val)
    delay_entry.grid(row=row_num, column=1, padx=5, pady=2)

    rows.append((key_combo, delay_entry))

def save_config():
    config = {
        "trigger": trigger_key.get(),
        "sequence": [(k.get(), d.get()) for k, d in rows]
    }
    file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
    if file:
        with open(file, "w") as f:
            json.dump(config, f, indent=4)

def load_config():
    file = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
    if not file:
        return
    with open(file, "r") as f:
        config = json.load(f)

    trigger_key.set(config.get("trigger", ""))

    # Clear old rows
    for k, d in rows:
        k.destroy()
        d.destroy()
    rows.clear()

    for key_val, delay_val in config.get("sequence", []):
        add_row(key_val, delay_val)

# --- GUI Layout ---
top_frame = ttk.Frame(root, padding=10)
top_frame.grid(row=0, column=0, sticky="ew")

ttk.Label(top_frame, text="Trigger key/button:").grid(row=0, column=0, sticky="w")
trigger_combo = ttk.Combobox(top_frame, textvariable=trigger_key, values=all_keys, state="readonly", width=20)
trigger_combo.grid(row=0, column=1, padx=5)
trigger_combo.current(0)

start_button = ttk.Button(top_frame, text="Start", command=start_macro)
start_button.grid(row=0, column=2, padx=5)

stop_button = ttk.Button(top_frame, text="Stop", command=stop_macro)
stop_button.grid(row=0, column=3, padx=5)

save_button = ttk.Button(top_frame, text="Save Config", command=save_config)
save_button.grid(row=0, column=4, padx=5)

load_button = ttk.Button(top_frame, text="Load Config", command=load_config)
load_button.grid(row=0, column=5, padx=5)

# Sequence area
frame = ttk.Frame(root, padding=10)
frame.grid(row=1, column=0)

ttk.Label(frame, text="Key").grid(row=0, column=0)
ttk.Label(frame, text="Delay (s)").grid(row=0, column=1)

add_button = ttk.Button(root, text="Add Key", command=add_row)
add_button.grid(row=2, column=0, pady=5)

# Add 1 default row
for _ in range(1):
    add_row()

root.mainloop()
