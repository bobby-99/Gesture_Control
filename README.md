# Cloud-Enabled Virtual Machine Interaction System using Hand Gesture Recognition

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green.svg" />
  <img src="https://img.shields.io/badge/TensorFlow-CNN-orange.svg" />
  <img src="https://img.shields.io/badge/AWS-EC2-yellow.svg" />
</p>

## 📌 Project Overview
This system allows users to control **AWS Cloud Infrastructure (EC2 Instances)** using **Hand Gestures** in real-time. It uses a Convolutional Neural Network (CNN) for gesture recognition and a FastAPI backend to trigger cloud actions.

### 🌟 Key Features
- **Touchless Control**: Start/Stop/Reboot servers with hand signs.
- **Smart Tracking**: Uses MediaPipe for hand skeleton tracking + Auto-Cropping.
- **Security Audit**: Real-time logging of all actions on a web dashboard.
- **Live Feedback**: Visual UI showing confidence scores and gesture mapping.

---

## 🛠️ Technology Stack (Why & What)

| Component | Technology | Why we used it? |
|-----------|------------|-----------------|
| **Frontend** | HTML5, CSS3, JavaScript | Lightweight dashboard to view logs and status. Polling architecture for real-time updates. |
| **Backend** | **FastAPI** (Python) | High-performance async API. Faster than Flask/Django for ML integration. |
| **Database** | **SQLite** (via SQLAlchemy) | Simple, zero-config database for storing Audit Logs. (Can swap to PostgreSQL easily). |
| **AI/ML** | **TensorFlow/Keras** | Built a custom CNN (Convolutional Neural Network) to classify images (64x64px). |
| **Vision** | **OpenCV** & **MediaPipe** | OpenCV for camera feed. MediaPipe for detecting hand landmarks (Skeleton) to crop background noise. |
| **Cloud** | **AWS SDK (Boto3)** | Python library to talk to AWS. Used to Start/Stop EC2 instances programmatically. |

---

## 📂 Project Structure

```
Chotu/
├── backend/                # Server & API
│   ├── main.py             # FastAPI App & Endpoints
│   ├── aws_manager.py      # Boto3 logic for AWS Control
│   ├── models.py           # Database Schema (AuditLog)
│   ├── requirements.txt    # Backend Dependencies
│   └── gesture_system.db   # (Auto-generated) Database file
├── frontend/               # Dashboard
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── app.js              # Logic (Fetch Logs, Status)
├── ml/                     # Machine Learning
│   ├── collect_data.py     # Tool to capture training images
│   ├── train_model.py      # Script to train the CNN
│   ├── run_recognition.py  # MAIN APP: Camera -> AI -> Backend
│   ├── class_map.txt       # Saves class order (Fist, Palm...)
│   └── gesture_model.h5    # The "Brain" (Trained Model)
└── legacy/                 # Archived old files
```

---

## 🚀 Installation & Setup Guide

### prerequisites
1.  **Python 3.9+** installed.
2.  **AWS Account** (Free Tier is fine) with Access Keys.
3.  **Webcam**.

### Step 1: Clone & Setup Dependencies
Open your terminal in the project folder:

```powershell
# 1. Install Libraries
pip install -r backend/requirements.txt
# (Make sure you also have opencv-python, mediapipe, tensorflow installed)
pip install opencv-python mediapipe tensorflow
```

### Step 2: Configure AWS Keys
Create a file named `.env` inside the `backend/` folder:
```ini
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
DATABASE_URL=sqlite:///./gesture_system.db
```
*(If you don't have AWS keys, the system runs in Demo Mode).*

---

## 🎮 How to Run (The "3-Terminal" Method)

You need to run 3 separate components simultaneously.

### Terminal 1: The Backend (Server)
This handles the logic and database.
```powershell
cd backend
uvicorn main:app --reload
```
*Wait until you see: "Application startup complete"*

### Terminal 2: The Frontend (Dashboard)
Simply open `frontend/index.html` in your browser.
*   You will see the "Audit Logs" and "AWS Status".

### Terminal 3: The AI (Vision Engine)
This opens the camera and detects gestures.
```powershell
python ml/run_recognition.py
```
*   A window "Smart Gesture Cloud Control" will appear.
*   A smaller "AI Input" window shows what the computer sees (Debugging).

---

## ✋ Supported Gestures & Actions

| Gesture | Action | Description |
|---------|--------|-------------|
| **OPEN PALM** ✋ | `START_INSTANCE` | Turns ON the server. |
| **FIST** ✊ | `STOP_INSTANCE` | Turns OFF the server. |
| **THUMB UP** 👍 | `REBOOT_INSTANCE` | Restarts the server. |
| **OK SIGN** 👌 | `ACKNOWLEDGE` | Logs an "Okay" (Safe Mode). |
| **NONE** (Empty) | `IGNORE` | Does nothing. |

---

## 🧠 Training Your Own Model (Optional)
If you want to retrain the AI for *your* hand:

1.  **Clear Data**: Delete `dataset/` and `ml/gesture_model.h5`.
2.  **Collect**: Run `python ml/collect_data.py`. Follow on-screen instructions.
    *   *Tip: For 'None', point camera at empty wall.*
3.  **Train**: Run `python ml/train_model.py`.

---

## ❓ Troubleshooting
*   **"Model predicts only Open Palm"**: Use the `AI Input` window to check lighting. Ensure you retrained if you deleted data.
*   **"Backend 500 Error"**: Delete `backend/gesture_system.db` and restart backend (Schema reset).
*   **"AWS Error"**: Check your `.env` keys.

---
**Developed by SoumyaRanjan** | *Cloud-Enabled Gesture System v2.0*
