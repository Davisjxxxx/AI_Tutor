# models_coach.py
from datetime import datetime, date
from sqlalchemy import (
    create_engine, Column, String, Integer, Text, Date, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from backend.database import Base

class Project(Base):
    __tablename__ = "project"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    milestone = Column(String)
    priority = Column(Integer, default=3)

class Task(Base):
    __tablename__ = "task"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("project.id"), index=True)
    title = Column(String, nullable=False)
    detail = Column(Text)
    status = Column(String, default="todo")  # todo|doing|done
    priority = Column(Integer, default=3)
    due_date = Column(Date)
    est_minutes = Column(Integer, default=25)
    created_at = Column(DateTime, default=datetime.utcnow)

class CheckIn(Base):
    __tablename__ = "checkin"
    id = Column(String, primary_key=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    type = Column(String, nullable=False)  # AM|PM
    what_learned = Column(Text)
    where_stuck = Column(Text)
    next_action = Column(Text)
    energy_1_5 = Column(Integer)

class Recall(Base):
    __tablename__ = "recall"
    id = Column(String, primary_key=True)
    for_date = Column(Date, default=date.today, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    project_id = Column(String, ForeignKey("project.id"))
    reviewed = Column(Boolean, default=False)

class Streak(Base):
    __tablename__ = "streak"
    date = Column(Date, primary_key=True)
    pomodoros = Column(Integer, default=0)
    shipped = Column(Boolean, default=False)
