import pyautogui
import os
import time

# ---------------- BASIC SYSTEM ACTIONS ----------------

def show_desktop():
    pyautogui.hotkey("win", "d")
    return {"action": "Show Desktop"}

def lock_screen():
    pyautogui.hotkey("win", "l")
    return {"action": "Screen Locked"}

def volume_up():
    pyautogui.press("volumeup")
    return {"action": "Volume Increased"}

def volume_down():
    pyautogui.press("volumedown")
    return {"action": "Volume Decreased"}

def open_explorer():
    pyautogui.hotkey("win", "e")
    return {"action": "File Explorer Opened"}

def task_manager():
    pyautogui.hotkey("ctrl", "shift", "esc")
    return {"action": "Task Manager Opened"}

def take_screenshot():
    ts = int(time.time())
    filename = f"screenshot_{ts}.png"
    pyautogui.screenshot(filename)
    return {"action": f"Screenshot saved as {filename}"}

def shutdown_prompt():
    os.system("shutdown /s /t 30")
    return {"action": "Shutdown in 30 seconds"}
