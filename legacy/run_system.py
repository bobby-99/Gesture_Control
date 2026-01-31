import os

print("1. Start Backend")
print("2. Start Gesture Recognition")

choice = input("Enter choice: ")

if choice == "1":
    os.system("python backend/app.py")
elif choice == "2":
    os.system("python gesture_recognition/gesture_detector.py")
