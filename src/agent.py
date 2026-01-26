"""
Main orchestrator - Coordinates the entire workflow
"""
from typing import Optional
from pathlib import Path

from .config import Config
from .transcript_processor import TranscriptProcessor, StudentDatabase
from .summarizer import LessonSummarizer
from .drive_client import DriveSlideRetriever
from .gmail_client import GmailSender, create_email_data


class LessonSummaryAgent:
    """Main agent that orchestrates the lesson summary workflow"""

    def __init__(self):
        self.config = Config()
        self.transcript_processor = TranscriptProcessor()
        self.summarizer = LessonSummarizer()
        self.drive_client = DriveSlideRetriever()
        self.gmail_client = GmailSender()
        self.student_db = StudentDatabase()

    def process_lesson(
        self,
        transcript_source: str,
        student_email: Optional[str] = None,
        create_draft: bool = None,
        sender_name: str = "Your Tutor"
    ) -> dict:
        """
        Main workflow: Process transcript -> Generate summary -> Find slides -> Send email

        Args:
            transcript_source: Path to transcript file or Fireflies meeting ID
            student_email: Student's email (if not in database)
            create_draft: Whether to create draft instead of sending (overrides config)
            sender_name: Name to sign email with

        Returns:
            dict with workflow results
        """
        print("🚀 Starting lesson summary workflow...")

        # Step 1: Load transcript
        print(f"\n📄 Loading transcript from: {transcript_source}")
        transcript_data = self._load_transcript(transcript_source)
        print(f"   ✓ Loaded lesson for {transcript_data.student_name}")
        print(f"   ✓ Date: {transcript_data.date}")
        print(f"   ✓ Topic: {transcript_data.topic}")

        # Step 2: Generate summary
        print(f"\n🤖 Generating AI summary using {self.config.AI_MODEL}...")
        summary = self.summarizer.generate_summary(transcript_data)
        print(f"   ✓ Summary generated")
        print(f"   ✓ Covered {len(summary.covered_topics)} topics")
        print(f"   ✓ {len(summary.key_vocabulary)} vocabulary items")

        # Step 3: Find slides
        print("\n🔍 Searching for class slides in Google Drive...")
        slide_data = self.drive_client.find_slides(
            student_name=transcript_data.student_name,
            date=transcript_data.date,
            topic=transcript_data.topic
        )

        if slide_data:
            print(f"   ✓ Found slides: {slide_data['name']}")
            slide_link = slide_data['webViewLink']
        else:
            print("   ⚠️  No slides found (email will be sent without slides)")
            slide_link = None

        # Step 4: Get student email
        if not student_email:
            student_email = self.student_db.get_student_email(transcript_data.student_name)

        if not student_email:
            raise ValueError(
                f"No email found for {transcript_data.student_name}. "
                "Please provide email via --email flag or add to students.json"
            )

        print(f"\n📧 Preparing email for {student_email}...")

        # Step 5: Create email data
        email_data = create_email_data(
            student_email=student_email,
            student_name=transcript_data.student_name,
            summary=summary,
            lesson_date=transcript_data.date,
            slide_link=slide_link,
            sender_name=sender_name
        )

        # Step 6: Send email or create draft
        should_create_draft = create_draft if create_draft is not None else not self.config.AUTO_SEND_EMAIL

        if should_create_draft:
            print("   Creating draft...")
            result = self.gmail_client.send_summary(email_data, create_draft=True)
            draft_url = self.gmail_client.get_draft_url(result['id'])
            print(f"   ✓ Draft created: {draft_url}")
        else:
            print("   Sending email...")
            result = self.gmail_client.send_summary(email_data, create_draft=False)
            print(f"   ✓ Email sent!")

        print("\n✅ Workflow completed successfully!\n")

        return {
            'status': 'success',
            'student': transcript_data.student_name,
            'email_status': result['status'],
            'email_id': result['id'],
            'summary': summary,
            'slides_found': slide_data is not None
        }

    def _load_transcript(self, source: str):
        """Load transcript from file or Fireflies"""
        # Check if it's a file path
        if Path(source).exists():
            return self.transcript_processor.load_from_file(source)

        # Check if it looks like a Fireflies ID
        if source.startswith('fireflies:') or len(source) == 24:  # Fireflies IDs are 24 chars
            meeting_id = source.replace('fireflies:', '')
            return self.transcript_processor.load_from_fireflies(meeting_id)

        # Try as file path one more time with transcripts folder
        full_path = self.config.TRANSCRIPTS_FOLDER / source
        if full_path.exists():
            return self.transcript_processor.load_from_file(str(full_path))

        raise ValueError(
            f"Could not load transcript from: {source}\n"
            "Provide either a file path or Fireflies meeting ID"
        )

    def preview_summary(self, transcript_source: str) -> dict:
        """
        Preview summary without sending email (for testing)
        """
        print("🔍 Preview mode - generating summary only...\n")

        transcript_data = self._load_transcript(transcript_source)
        print(f"Student: {transcript_data.student_name}")
        print(f"Date: {transcript_data.date}")
        print(f"Topic: {transcript_data.topic}\n")

        summary = self.summarizer.generate_summary(transcript_data)

        print("📚 WHAT WE COVERED TODAY")
        for i, topic in enumerate(summary.covered_topics, 1):
            print(f"{i}. {topic}")

        print("\n🔑 KEY VOCABULARY")
        for term, definition in summary.key_vocabulary.items():
            print(f"• {term}: {definition}")

        print(f"\n🌟 YOUR PROGRESS")
        print(summary.progress_note)

        print("\n📝 PRACTICE SUGGESTIONS")
        for i, task in enumerate(summary.homework, 1):
            print(f"{i}. {task}")

        return {
            'transcript_data': transcript_data,
            'summary': summary
        }
