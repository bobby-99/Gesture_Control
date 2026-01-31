from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Connect to SQLite for local development (cost-free), easy switch to Postgres
# For Production/Viva: Use Postgres URL if available
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gesture_system.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # 'admin' or 'user'
    is_active = Column(Boolean, default=True)

class GestureAction(Base):
    __tablename__ = "gesture_actions"
    id = Column(Integer, primary_key=True, index=True)
    gesture_name = Column(String, unique=True, index=True) # e.g., "FIST", "OPEN_PALM"
    aws_action = Column(String) # e.g., "STOP_INSTANCE", "START_INSTANCE"
    description = Column(String)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String) # e.g., "INSTANCE_STOPPED"
    gesture_detected = Column(String) # NEW: Store the raw gesture name
    target_resource = Column(String) # e.g., "i-0123456789abcdef0"
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String) # "SUCCESS", "FAILED"

    user = relationship("User")

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
