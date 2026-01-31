def identify_gesture(landmarks):
    # Simple logic using index finger
    if landmarks[8].y < landmarks[6].y:
        return "OPEN_PALM"
    else:
        return "FIST"
