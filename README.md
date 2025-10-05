🖱️ MacroTool — Powerful Windows Macro Creator

Automate your keyboard and mouse with precision, speed, and full control.

MacroTool is a lightweight Windows utility that lets you bind any key or mouse button to a custom sequence of actions. Configure complex macros, adjust timing between key presses, and save/load your setups — all with an intuitive interface.

✨ Features

🎛️ GUI-based macro editor — no scripting required

🖱️ Mouse and keyboard input support (MB1–MB8, all keys)

⏱️ Adjustable delay per key — fine-tune your timing

💾 Save/Load configurations as .json files

🔄 Persistent AppData storage for clean setups

🧩 Automatic detection of mouse buttons via the included Input Listener

⚙️ Installer-ready (Inno Setup compatible) — deploy like a real Windows app

🧠 How it works

The Button Listener captures your mouse button layout and saves it to
%APPDATA%\MacroTool\mouse_buttons.json.

The Macro Tool GUI loads that config, letting you assign sequences to any trigger.

Your saved macros can be instantly executed with your chosen trigger key/button.

🏗️ Built With

Python 3.13

tkinter — for the clean and lightweight GUI

keyboard, pynput, pyautogui — for system-wide input handling

pygame — for mouse button analysis

json — for portable configuration files

Inno Setup — for packaging a user-friendly installer

💡 Ideal for gamers, productivity power-users, and anyone who wants complete control over input automation.
