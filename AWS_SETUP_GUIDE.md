# AWS Setup & Integration Guide (Free Tier)

This guide will help you set up an **Amazon Web Services (AWS)** account and connect it to your project without spending money.

---

## Phase 1: Create a Free AWS Account

1.  **Go to AWS Signup**:
    *   Visit [aws.amazon.com/free](https://aws.amazon.com/free).
    *   Click **"Create a Free Account"**.
2.  **Fill Details**:
    *   Email, Password, AWS Account Name (e.g., `GestureProjectAdmin`).
    *   **Verification**: You will need a Credit/Debit Card for identity verification. **They will charge ~$1 (₹2) and refund it immediately.** This is standard.
    *   **Select Plan**: Choose **"Basic Support - Free"**.

3.  **Login**:
    *   Go to the **AWS Console**.
    *   Sign in as "Root User".

---

## Phase 2: Create "Access Keys" (The Password for your Code)

**CRITICAL SECURITY WARNING**: Never share these keys on GitHub. They give full access to your account.

1.  **Open IAM Dashboard**:
    *   In the top search bar, type **"IAM"** and click "IAM".
2.  **Create a User**:
    *   Click **"Users"** -> **"Create user"**.
    *   Username: `GestureBot`.
    *   Click **Next**.
3.  **Set Permissions (The "Policy")**:
    *   Select **"Attach policies directly"**.
    *   Search for `AmazonEC2FullAccess`. Check the box. (For Viva, this is easiest. In real life, we'd restrict this more).
    *   Search for `AmazonS3FullAccess`. Check the box.
    *   Click **Next** -> **Create user**.
4.  **Generate Keys**:
    *   Click on the newly created user `GestureBot`.
    *   Go to the **"Security credentials"** tab.
    *   Scroll down to **"Access keys"**.
    *   Click **"Create access key"**.
    *   Select **"Local code"**. Check the verification box. Click **Next**.
    *   **DOWNLOAD THE .CSV FILE NOW.** You will define see the Secret Key again.
    *   You now have an `Access Key ID` (e.g., `AKIA...`) and a `Secret Access Key` (e.g., `wJalr...`).

---

## Phase 3: Integrate into Your Project

Now we tell your Python Backend how to talk to AWS.

1.  **Locate the Config File**:
    *   Go to your project folder: `c:\Users\ichotu\Desktop\Chotu\backend`.
    *   Look for a file named `.env.example`.
    *   **Rename** it to `.env` (just `.env`, no `.txt`).

2.  **Edit `.env`**:
    *   Open `.env` in Notepad or VS Code.
    *   Paste your keys like this:

    ```ini
    AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE  <-- Your Key ID
    AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY <-- Your Secret Key
    AWS_REGION=us-east-1
    DATABASE_URL=sqlite:///./gesture_system.db
    ```

3.  **Launch an EC2 Instance (To Control)**:
    *   Go back to AWS Console -> Search "EC2".
    *   Click **"Launch Instance"**.
    *   Name: `Gesture-Test-VM`.
    *   OS: **Ubuntu** (Free Tier Eligible).
    *   Instance Type: **t2.micro** (Free Tier Eligible).
    *   Key Pair: Select "Proceed without a key pair" (Since we are only starting/stopping it, not logging in via SSH).
    *   Click **"Launch Instance"**.
    *   Copy the **Instance ID** (e.g., `i-0123456789abcdef0`).

---

## Phase 4: Test It

1.  Start your Backend: `uvicorn main:app --reload` (inside `backend/`).
2.  Open your Frontend: `frontend/index.html`.
3.  You should see your new Instance listed!
4.  Show a **FIST** to the camera -> The Instance state should change to `STOPPING` on the dashboard.

**🎉 Upgrade Complete.**
