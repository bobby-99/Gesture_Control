import cv2
import mediapipe as mp
import requests
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def finger_up(lm, tip, pip):
    return lm[tip].y < lm[pip].y

def detect_gesture(lm):
    # Only 4 fingers for counting (IGNORE THUMB)
    index = finger_up(lm, 8, 6)
    middle = finger_up(lm, 12, 10)
    ring = finger_up(lm, 16, 14)
    pinky = finger_up(lm, 20, 18)

    fingers = [index, middle, ring, pinky]
    count = fingers.count(True)

    # ---- CORE COMPUTER OPERATIONS ----
    if count == 0:
        return "FIST"          # Stop VM

    if count == 4:
        return "OPEN_PALM"     # Start VM

    if count == 1 and index:
        return "ONE"           # CPU scale up

    if count == 2 and index and middle:
        return "TWO"           # Restart VM

    if count == 3:
        return "THREE"         # RAM increase

    # ---- SPECIAL GESTURES ----
    # Thumb Up
    thumb_up = lm[4].y < lm[3].y
    if thumb_up and count == 0:
        return "THUMB_UP"

    # OK Sign
    dist = math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y)
    if dist < 0.035 and middle and ring and pinky:
        return "OK_SIGN"

    return "UNKNOWN"

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "NO HAND"

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand.landmark)

            try:
                requests.post(
                    "http://127.0.0.1:5000/gesture",
                    json={"gesture": gesture},
                    timeout=0.2
                )
            except:
                pass

    # DISPLAY (BIG & CLEAR)
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 90), (0, 0, 0), -1)
    cv2.putText(
        frame,
        f"GESTURE : {gesture}",
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.6,
        (0, 255, 0),
        3
    )

    cv2.imshow("Computer-Controlled Gesture System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
