"""
Lesson Summary Agent - Main Package
"""

__version__ = "1.0.0"

from .agent import LessonSummaryAgent
from .config import Config
from .models import LessonSummary, TranscriptData, StudentInfo, EmailData

__all__ = [
    'LessonSummaryAgent',
    'Config',
    'LessonSummary',
    'TranscriptData',
    'StudentInfo',
    'EmailData',
]
