"""
Configuration management for Lesson Summary Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # AI Settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL", "gemini-1.5-pro")

    # Google Settings
    GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
    SLIDES_FOLDER_ID = os.getenv("SLIDES_FOLDER_ID")

    # Optional: Fireflies
    FIREFLIES_API_KEY = os.getenv("FIREFLIES_API_KEY")

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    TRANSCRIPTS_FOLDER = BASE_DIR / os.getenv("TRANSCRIPTS_FOLDER", "transcripts")
    STUDENT_DB_PATH = BASE_DIR / os.getenv("STUDENT_DB_PATH", "students.json")
    CREDENTIALS_FILE = BASE_DIR / "credentials.json"
    TOKEN_FILE = BASE_DIR / "token.json"

    # Email Settings
    AUTO_SEND_EMAIL = os.getenv("AUTO_SEND_EMAIL", "false").lower() == "true"

    # Google API Scopes
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/drive.readonly'
    ]

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []

        if cls.AI_MODEL.startswith("gemini") and not cls.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY is required for Gemini models")

        if cls.AI_MODEL.startswith("claude") and not cls.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY is required for Claude models")

        if not cls.GMAIL_SENDER_EMAIL:
            errors.append("GMAIL_SENDER_EMAIL is required")

        if not cls.CREDENTIALS_FILE.exists():
            errors.append(f"Google credentials file not found at {cls.CREDENTIALS_FILE}")

        return errors

    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        cls.TRANSCRIPTS_FOLDER.mkdir(parents=True, exist_ok=True)
