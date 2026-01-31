from computer_gestures import *

current_status = {"last_action": "None"}

def process_gesture(gesture):
    print("Gesture received:", gesture)

    if gesture == "OPEN_PALM":
        current_status["last_action"] = "Show Desktop"
        return show_desktop()

    elif gesture == "FIST":
        current_status["last_action"] = "Lock Screen"
        return lock_screen()

    elif gesture == "ONE":
        current_status["last_action"] = "Volume Up"
        return volume_up()

    elif gesture == "TWO":
        current_status["last_action"] = "Volume Down"
        return volume_down()

    elif gesture == "THREE":
        current_status["last_action"] = "Open File Explorer"
        return open_explorer()

    elif gesture == "FOUR":
        current_status["last_action"] = "Open Task Manager"
        return task_manager()

    elif gesture == "THUMB_UP":
        current_status["last_action"] = "Screenshot"
        return take_screenshot()

    elif gesture == "OK_SIGN":
        current_status["last_action"] = "Shutdown"
        return shutdown_prompt()

    else:
        return {"action": "No action"}

def get_status():
    return current_status