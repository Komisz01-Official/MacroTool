import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys

# Get the folder where controller.exe (or controller.py) is running
BASE_DIR = os.path.dirname(sys.argv[0])

MACRO_EXE = os.path.join(BASE_DIR, "macro_tool_v.0.5_(json).exe")
LISTENER_EXE = os.path.join(BASE_DIR, "button_press_listener_v.0.2.exe")

def run_macro():
    if os.path.exists(MACRO_EXE):
        subprocess.Popen([MACRO_EXE])
    else:
        print("❌ Macro Tool EXE not found!")

def run_listener():
    if os.path.exists(LISTENER_EXE):
        subprocess.Popen([LISTENER_EXE])
    else:
        print("❌ Button Listener EXE not found!")

# GUI setup
root = tk.Tk()
root.title("Komisz_01's Macro Controller")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="🎮 Macro Controller", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

ttk.Button(frame, text="▶ Run Macro Tool", command=run_macro, width=30).grid(row=1, column=0, pady=5)
ttk.Button(frame, text="🖱 Run Button Listener", command=run_listener, width=30).grid(row=2, column=0, pady=5)

root.mainloop()
