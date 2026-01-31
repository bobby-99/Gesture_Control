import cv2
import os
import mediapipe as mp
import numpy as np
import time

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

def create_dataset_dirs(base_path, gestures):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    for gesture in gestures:
        path = os.path.join(base_path, gesture)
        if not os.path.exists(path):
            os.makedirs(path)

def capture_images(gesture_name, num_samples=200):
    cap = cv2.VideoCapture(0)
    count = 0
    save_path = f"dataset/{gesture_name}"
    last_capture_time = 0
    capturing = False
    
    print(f"\n[INSTRUCTION] SHOW YOUR HAND for '{gesture_name}'")
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # 1. Hand Detection
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        
        display_frame = frame.copy()
        hand_found = False
        
        # Special handling for 'none' (Capture Background/No Hand)
        if gesture_name == "none":
             if capturing:
                current_time = time.time()
                if current_time - last_capture_time > 0.5:
                    # Just capture the center crop of the screen as 'background'
                    h, w, c = frame.shape
                    # Center 300x300 crop
                    cx, cy = w//2, h//2
                    bg_img = frame[cy-150:cy+150, cx-150:cx+150]
                    if bg_img.size > 0:
                        bg_img = cv2.resize(bg_img, (64, 64))
                        cv2.imwrite(f"{save_path}/{gesture_name}_{count}.jpg", bg_img)
                        count += 1
                        last_capture_time = current_time
             cv2.putText(display_frame, "Point at wall/empty space", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Standard Hand Detection for other gestures
        elif result.multi_hand_landmarks:
            hand_found = True
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw landmarks (Visual Feedback)
                mp_draw.draw_landmarks(display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
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
                
                # Add padding
                padding = 40
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)

                # CROP the hand
                if count < num_samples and capturing:
                    current_time = time.time()
                    if current_time - last_capture_time > 0.5: # Slow down: 1 photo every 0.5s
                        try:
                            hand_img = frame[y_min:y_max, x_min:x_max]
                            if hand_img.size > 0:
                                hand_img = cv2.resize(hand_img, (64, 64))
                                cv2.imwrite(f"{save_path}/{gesture_name}_{count}.jpg", hand_img)
                                count += 1
                                last_capture_time = current_time
                        except:
                            pass
                    
                cv2.rectangle(display_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        status_text = f"Captured: {count}/{num_samples}"
        if not hand_found:
            status_text += " (NO HAND DETECTED)"
            
        cv2.putText(display_frame, f"Gesture: {gesture_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(display_frame, status_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        if not capturing:
            cv2.putText(display_frame, "Press 's' to start", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        cv2.imshow("Smart Data Collector", display_frame)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            capturing = True
        if key & 0xFF == ord('q'):
            break
        if count >= num_samples:
            break
            
    cap.release()
    cv2.destroyAllWindows()

capturing = False # Global flag

if __name__ == "__main__":
    gestures = ["fist", "open_palm", "thumb_up", "ok_sign", "none"]
    create_dataset_dirs("dataset", gestures)
    
    print("--- SMART CROP DATASET COLLECTOR ---")
    for gesture in gestures:
        capturing = False
        if gesture == "none":
            print("\n[INFO] For 'none', just capture the background (no hand).")
        capture_images(gesture)
        
    print("\n[DONE] Dataset upgraded with cropped hands. Now run 'ml/train_model.py'!")
