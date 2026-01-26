"""
Data models for lesson summary system using Pydantic
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class LessonSummary(BaseModel):
    """Structured lesson summary output"""
    covered_topics: List[str] = Field(
        description="3-5 main topics covered in the lesson",
        min_items=3,
        max_items=5
    )
    key_vocabulary: Dict[str, str] = Field(
        description="Key terms with their definitions (max 10)",
    )
    progress_note: str = Field(
        description="One encouraging sentence about student's progress"
    )
    homework: List[str] = Field(
        description="2-3 specific practice suggestions",
        min_items=2,
        max_items=3
    )


class TranscriptData(BaseModel):
    """Transcript data structure"""
    student_name: str
    date: str
    topic: str
    content: str
    duration_minutes: Optional[int] = None
    student_level: Optional[str] = None  # e.g., "beginner", "intermediate"


class StudentInfo(BaseModel):
    """Student information"""
    name: str
    email: str
    level: Optional[str] = None
    preferred_language: str = "English"
    notes: Optional[str] = None


class EmailData(BaseModel):
    """Email composition data"""
    to_email: str
    student_name: str
    subject: str
    summary: LessonSummary
    slide_link: Optional[str]
    lesson_date: str
    sender_name: str = "Your Tutor"
