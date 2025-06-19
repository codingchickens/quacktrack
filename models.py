from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, create_engine
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(String, primary_key=True)  # CRM-style ID
    name = Column(String)
    preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sessions = relationship("Session", back_populates="student")

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey('students.id'))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    state = Column(JSON)
    
    student = relationship("Student", back_populates="sessions")
    interactions = relationship("Interaction", back_populates="session")
    security_logs = relationship("SecurityLog", back_populates="session")

class Interaction(Base):
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey('sessions.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_text = Column(String)
    response_text = Column(String)
    agent_used = Column(String)
    language = Column(String)
    
    session = relationship("Session", back_populates="interactions")

class SecurityLog(Base):
    __tablename__ = 'security_logs'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey('sessions.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)
    details = Column(JSON)
    
    session = relationship("Session", back_populates="security_logs")

def init_db(db_url: str = "sqlite:///learning_sessions.db"):
    """Initialize the database and create all tables."""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine) 