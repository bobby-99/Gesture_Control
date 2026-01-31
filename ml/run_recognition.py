import cv2
import numpy as np
import tensorflow as tf
import requests
import time
import mediapipe as mp
import os

# Configuration
API_URL = "http://127.0.0.1:8000/control/execute"
MODEL_PATH = "ml/gesture_model.h5"

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

def main():
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("[INFO] Model loaded successfully.")
    except:
        print(f"[ERROR] Could not load model. Did you run train_model.py?")
        return

    # Dynamic Class Loading to prevent mismatches
    import ast
    class_map_path = "ml/class_map.txt"
    if os.path.exists(class_map_path):
        with open(class_map_path, "r") as f:
            mapping = ast.literal_eval(f.read())
            # mapping is {'fist': 0, ...} -> We need ['fist', ...] sorted by index
            class_names = [k for k, v in sorted(mapping.items(), key=lambda item: item[1])]
            print(f"[INFO] Loaded Class Map: {class_names}")
    else:
        print("[WARNING] class_map.txt not found. Using alphabetical default.")
        class_names = ["fist", "none", "ok_sign", "open_palm", "thumb_up"] 
    
    cap = cv2.VideoCapture(0)
    last_api_call = 0
    
    print("[INFO] Starting Smart Recognition...")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. Hand Detection
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        
        gesture = "none"
        confidence = 0.0
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw Skeleton (What user asked for)
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract Bounding Box
                h, w, c = frame.shape
                x_min, y_min = w, h
                x_max, y_max = 0, 0
                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)
                
                # Padding
                padding = 40
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)
                
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                
                try:
                    hand_img = frame[y_min:y_max, x_min:x_max]
                    if hand_img.size > 0:
                        hand_img = cv2.resize(hand_img, (64, 64))
                        
                        # CRITICAL FIX: Convert BGR (OpenCV) to RGB (Training Format)
                        hand_img = cv2.cvtColor(hand_img, cv2.COLOR_BGR2RGB)
                        
                        hand_img = hand_img / 255.0
                        hand_img = np.expand_dims(hand_img, axis=0)
                        
                        # DEBUG: Show what the model sees
                        cv2.imshow("AI Input (64x64)", cv2.resize(hand_img[0], (200, 200))) # Resize for visibility

                        predictions = model.predict(hand_img, verbose=0)
                        confidence = np.max(predictions)
                        class_idx = np.argmax(predictions)
                        gesture = class_names[class_idx]
                        
                        # DEBUG: Print all probs
                        # print(f"Probs: {predictions[0]}")
                except:
                    pass
        else:
             # No hand -> automatically none
             gesture = "none"

        # UI
        color = (0, 255, 0) if gesture != "none" else (0, 0, 255)
        label = f"{gesture.upper()} ({confidence*100:.1f}%)"
        cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        cv2.imshow("Smart Gesture Cloud Control", frame)

        # Logic: Only send if gesture is NOT none and confident
        current_time = time.time()
        if gesture != "none" and confidence > 0.8:
            if current_time - last_api_call > 3.0:
                print(f"[ACTION] Sending {gesture} to Cloud...")
                try:
                    # Async request (fire and forget wrapper ideally, but simple timeout here)
                    requests.post(API_URL, json={"gesture": gesture}, timeout=0.1)
                except:
                    pass
                last_api_call = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
