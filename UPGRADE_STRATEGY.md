# UPGRADE STRATEGY: Cloud-Enabled Gesture Control System (AWS + FastAPI + CNN)

## 1. Executive Summary: From "Weak Script" to "Enterprise System"

We are upgrading this project from a local, script-based prototype to a **professional, cloud-native architecture** utilizing **AWS (Amazon Web Services)**.

### Upgrade Roadmap

| Feature | Current (Weak) State | **Target (Strong) Enterprise State** |
| :--- | :--- | :--- |
| **Architecture** | Monolithic Python Scripts | **Microservices** (Frontend <-> API <-> ML Service) |
| **Backend** | Flask (Basic/Blocking) | **FastAPI** (Async, High-Performance, auto-docs) |
| **Database** | None / In-Memory | **PostgreSQL** (Relational Data, Audit Logs, User Mgmt) |
| **AI Model** | Hardcoded Rules (If/Else) | **Convolutional Neural Network (CNN)** (Deep Learning) |
| **Cloud** | None | **AWS EC2** (Control), **S3** (Storage), **IAM** (Security) |
| **Security** | None | **JWT Authentication** & **Role-Based Access Control** |

---

## 2. AWS Fundamentals (Viva Defense)

**Concept**: In this project, the Local Machine acts as an "Edge Device" (IoT) and AWS is the "Central Cloud".

### 2.1 EC2 (Elastic Compute Cloud) - *The "Virtual Machine"*
*   **What it is**: A scalable virtual computer hosted in AWS data centers.
*   **Our Use Case**: The system will remotely control these instances (Start/Stop/Reboot) based on hand gestures.
*   **Why**: Demonstrates **Infrastructure as Code (IaC)**. Controlling a real remote server is technically superior to local scripts.

### 2.2 S3 (Simple Storage Service) - *The "Cloud Hard Drive"*
*   **What it is**: Object storage built to store and retrieve any amount of data.
*   **Our Use Case**: We store **Execution Logs**, **Security Audit Trails**, and **Model Checkpoints**.
*   **Why**: Provides an immutable, tamper-proof record of all actions (Critical for security audits).

### 2.3 IAM (Identity Access Management) - *The "Security Guard"*
*   **What it is**: The system that manages permissions (Who can do what).
*   **Our Use Case**: We verify that the API has permission to *start* an instance but not *terminate* (delete) it.
*   **Why**: **Least Privilege Principle**. Prevents catastrophic accidents from a wrong gesture.

### 2.4 Boto3 - *The "Connector"*
*   **What it is**: The official AWS SDK for Python.
*   **Our Use Case**: The bridge between our FastAPI backend and the AWS Cloud API.

---

## 3. System Architecture

```mermaid
graph TD
    User[User @ Webcam] -->|Images| CV_Mod[Gesture Recognition Module]
    CV_Mod -->|Landmarks| CNN[CNN Model (Local)]
    CNN -->|Predicted Class| CMD_Map[Command Mapper]
    CMD_Map -->|API Request| Backend[FastAPI Backend]
    
    subgraph "Cloud Backend Service"
        Backend -->|Auth| JWT[JWT Auth]
        Backend -->|Query| DB[(PostgreSQL)]
        Backend -->|Log Audit| S3[AWS S3]
        Backend -->|Control| AWS_SDK[Boto3 Controller]
    end
    
    subgraph "AWS Infrastructure"
        AWS_SDK -->|Start/Stop| EC2[EC2 Instances]
        AWS_SDK -->|Read Status| CloudWatch[CloudWatch Metrics]
    end
```

## 4. Database Schema (PostgreSQL)

We will implement a relational schema to track every interaction.

1.  **`users`**:
    *   `id`, `username`, `password_hash`, `role` (Admin/User).
    *   *Purpose*: Security. Only Admins can execute critical AWS commands.
2.  **`gestures`**:
    *   `id`, `name` (e.g., "FIST"), `aws_action` (e.g., "STOP_INSTANCE").
    *   *Purpose*: Configurable mapping.
3.  **`audit_logs`**:
    *   `id`, `user_id`, `gesture_detected`, `action_taken`, `s3_log_url`, `timestamp`.
    *   *Purpose*: "Who did what and when?" (Crucial for Viva).

## 5. Security Protocols (Critical)

*   **Token-Based Header Auth**: Every API request must carry a valid `Bearer Token`.
*   **Audit Logging**: Every command is logged to PostgreSQL and mirrored to S3.
*   **Safety Interlocks**:
    *   "Critical Actions" (Shutdown) require a 2-step gesture combo or hold-time.
