from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import models
from models import SessionLocal, engine, AuditLog, User
from aws_manager import AWSService
import datetime

# Initialize Database
models.init_db()

app = FastAPI(title="Gesture Control Cloud System", version="2.0")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

aws_client = AWSService()

# --- Pydantic Schemas ---
class GestureCommand(BaseModel):
    gesture: str
    target_instance_id: Optional[str] = None

class AWSStatus(BaseModel):
    id: str
    type: str
    state: str
    public_ip: str

# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "Cloud-Enabled Gesture System Online", "status": "active"}

@app.get("/aws/instances", response_model=List[AWSStatus])
def list_instances(db: Session = Depends(get_db)):
    """Fetch live status of EC2 instances from AWS."""
    return aws_client.get_instances()

@app.post("/control/execute")
def execute_command(cmd: GestureCommand, db: Session = Depends(get_db)):
    """
    Execute AWS command based on gesture.
    Safe-guarded to Free Tier actions (Start/Stop).
    """
    gesture = cmd.gesture.upper()
    instance_id = cmd.target_instance_id

    # If no instance ID provided, pick the first one (Demo mode)
    if not instance_id:
        instances = aws_client.get_instances()
        if instances:
            instance_id = instances[0]['id']
        else:
            # If no AWS credentials or no instances, use a dummy ID for the log
            instance_id = "i-demo-12345"

    action_result = {}
    db_action = "UNMAPPED_GESTURE" # Default if no match

    if gesture == "OPEN_PALM":
        action_result = aws_client.start_instance(instance_id)
        db_action = "START_INSTANCE"
    elif gesture == "FIST":
        action_result = aws_client.stop_instance(instance_id)
        db_action = "STOP_INSTANCE"
    elif gesture == "THUMB_UP":
        # Mapping: Reboot VM
        action_result = aws_client.reboot_instance(instance_id)
        db_action = "REBOOT_INSTANCE"
    elif gesture == "OK_SIGN":
        # Mapping: Safe Acknowledge
        # action_result = aws_client.terminate_instance(instance_id) # TOO DANGEROUS
        db_action = "OK_ACKNOWLEDGED"
        action_result = {"status": "acknowledged", "message": "OK Sign Received - No Action Taken"}
    else:
        return {"status": "ignored", "reason": "Unknown Gesture"}
    
    # Log to Database even if unmapped, so we see what's happening
    log = AuditLog(
        user_id=1,
        action=db_action, 
        target_resource=instance_id,
        gesture_detected=gesture, # Add this field to the model if missing, or handle in log
        status="SUCCESS" if "error" not in action_result else "FAILED",
        timestamp=datetime.datetime.utcnow()
    )
    db.add(log)
    db.commit()

    # Log to Database
    try:
        log = AuditLog(
            user_id=1,
            action=db_action, 
            target_resource=instance_id,
            gesture_detected=gesture, 
            status="SUCCESS" if "error" not in action_result else "FAILED",
            timestamp=datetime.datetime.utcnow()
        )
        db.add(log)
        db.commit()
        print(f"[DB LOG] Gesture: {gesture} -> Action: {db_action}")
    except Exception as e:
        print(f"[DB ERROR] Failed to log: {e}")

    return {"gesture": gesture, "aws_response": action_result, "action_mapped": db_action}

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(10).all()
    return logs
