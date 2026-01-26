"""
Transcript parsing and data extraction module
"""
import re
import json
from pathlib import Path
from typing import Dict, Optional
import requests

from .models import TranscriptData, StudentInfo
from .config import Config


class TranscriptProcessor:
    """Handles transcript loading and parsing"""

    def __init__(self):
        self.config = Config()

    def load_from_file(self, file_path: str) -> TranscriptData:
        """
        Load transcript from local file.
        Expected filename format: YYYY-MM-DD_StudentName_Topic.txt
        Example: 2026-01-05_JohnDoe_GrammarLesson.txt
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Transcript file not found: {file_path}")

        # Parse filename
        filename = path.stem
        metadata = self._parse_filename(filename)

        # Read content
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get student info if available
        student_info = self._get_student_info(metadata['student_name'])

        return TranscriptData(
            student_name=metadata['student_name'],
            date=metadata['date'],
            topic=metadata['topic'],
            content=content,
            student_level=student_info.level if student_info else None
        )

    def _parse_filename(self, filename: str) -> Dict[str, str]:
        """
        Parse structured filename.
        Supports formats:
        - YYYY-MM-DD_StudentName_Topic
        - StudentName_Topic_YYYY-MM-DD
        """
        # Try primary format: YYYY-MM-DD_StudentName_Topic
        pattern1 = r'(\d{4}-\d{2}-\d{2})_([^_]+)_(.+)'
        match = re.match(pattern1, filename)

        if match:
            return {
                'date': match.group(1),
                'student_name': match.group(2).replace('_', ' '),
                'topic': match.group(3).replace('_', ' ')
            }

        # Try alternative format: StudentName_Topic_YYYY-MM-DD
        pattern2 = r'([^_]+)_(.+?)_(\d{4}-\d{2}-\d{2})'
        match = re.match(pattern2, filename)

        if match:
            return {
                'student_name': match.group(1).replace('_', ' '),
                'topic': match.group(2).replace('_', ' '),
                'date': match.group(3)
            }

        # Fallback: try to extract any date
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
        parts = filename.split('_')

        return {
            'date': date_match.group(0) if date_match else 'Unknown',
            'student_name': parts[0].replace('_', ' ') if parts else 'Unknown',
            'topic': parts[1].replace('_', ' ') if len(parts) > 1 else 'General Lesson'
        }

    def _get_student_info(self, student_name: str) -> Optional[StudentInfo]:
        """Load student info from database if available"""
        if not self.config.STUDENT_DB_PATH.exists():
            return None

        try:
            with open(self.config.STUDENT_DB_PATH, 'r') as f:
                students_db = json.load(f)

            # Case-insensitive search
            student_name_lower = student_name.lower()
            for student_data in students_db.get('students', []):
                if student_data['name'].lower() == student_name_lower:
                    return StudentInfo(**student_data)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load student database: {e}")

        return None

    def load_from_fireflies(self, meeting_id: str) -> TranscriptData:
        """
        Load transcript from Fireflies.ai API
        Requires FIREFLIES_API_KEY in environment
        """
        if not self.config.FIREFLIES_API_KEY:
            raise ValueError("FIREFLIES_API_KEY not configured")

        url = "https://api.fireflies.ai/graphql"
        headers = {
            "Authorization": f"Bearer {self.config.FIREFLIES_API_KEY}",
            "Content-Type": "application/json"
        }

        query = """
        query Transcript($transcriptId: String!) {
          transcript(id: $transcriptId) {
            title
            date
            duration
            sentences {
              text
              speaker_name
            }
          }
        }
        """

        response = requests.post(
            url,
            json={"query": query, "variables": {"transcriptId": meeting_id}},
            headers=headers
        )

        if response.status_code != 200:
            raise Exception(f"Fireflies API error: {response.text}")

        data = response.json()['data']['transcript']

        # Reconstruct transcript from sentences
        transcript_text = "\n".join([
            f"{s['speaker_name']}: {s['text']}"
            for s in data['sentences']
        ])

        # Extract student name from title (assuming format: "Lesson with John Doe")
        title = data['title']
        student_name = self._extract_student_name_from_title(title)

        return TranscriptData(
            student_name=student_name,
            date=data['date'][:10],  # Extract YYYY-MM-DD
            topic=title,
            content=transcript_text,
            duration_minutes=data['duration']
        )

    def _extract_student_name_from_title(self, title: str) -> str:
        """Extract student name from Fireflies meeting title"""
        # Common patterns: "Lesson with John", "John - English Class"
        patterns = [
            r'with\s+(.+?)(?:\s*-|$)',
            r'^(.+?)\s*-',
            r'Lesson:\s*(.+?)(?:\s*-|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return "Student"  # Default fallback


class StudentDatabase:
    """Manage student information"""

    def __init__(self):
        self.config = Config()
        self.db_path = self.config.STUDENT_DB_PATH

    def get_student_email(self, student_name: str) -> Optional[str]:
        """Get student email from database"""
        if not self.db_path.exists():
            return None

        try:
            with open(self.db_path, 'r') as f:
                students_db = json.load(f)

            student_name_lower = student_name.lower()
            for student in students_db.get('students', []):
                if student['name'].lower() == student_name_lower:
                    return student['email']

        except (json.JSONDecodeError, KeyError):
            pass

        return None

    def create_sample_database(self):
        """Create a sample student database"""
        sample_data = {
            "students": [
                {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "level": "intermediate",
                    "preferred_language": "English",
                    "notes": "Focusing on business English"
                },
                {
                    "name": "Jane Smith",
                    "email": "jane.smith@example.com",
                    "level": "beginner",
                    "preferred_language": "English",
                    "notes": "New student, very motivated"
                }
            ]
        }

        with open(self.db_path, 'w') as f:
            json.dump(sample_data, f, indent=2)

        print(f"Sample student database created at {self.db_path}")
