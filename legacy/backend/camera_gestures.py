import cv2
import mediapipe as mp
import requests

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

TIP_IDS = [4, 8, 12, 16, 20]

def send(gesture):
    try:
        requests.post(
            "http://127.0.0.1:5000/gesture",
            json={"gesture": gesture},
            timeout=0.1
        )
    except:
        pass

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "NONE"

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        fingers = []

        # THUMB
        if lm[TIP_IDS[0]].x < lm[TIP_IDS[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # OTHER FINGERS
        for i in range(1, 5):
            if lm[TIP_IDS[i]].y < lm[TIP_IDS[i] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total = sum(fingers)

        if total == 0:
            gesture = "FIST"
        elif total == 1:
            gesture = "ONE"
        elif total == 2:
            gesture = "TWO"
        elif total == 3:
            gesture = "THREE"
        elif total == 4:
            gesture = "FOUR"
        elif total == 5:
            gesture = "OPEN_PALM"

        send(gesture)

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Gesture Camera", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
