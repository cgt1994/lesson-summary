"""
Gmail integration for sending lesson summaries
"""
from typing import Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import EmailData, LessonSummary
from .config import Config


class GmailSender:
    """Send lesson summaries via Gmail API"""

    def __init__(self):
        self.config = Config()
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API"""
        # Reuse Drive credentials since they include Gmail scope
        if self.config.TOKEN_FILE.exists():
            self.creds = Credentials.from_authorized_user_file(
                str(self.config.TOKEN_FILE),
                self.config.SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not self.config.CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Google credentials file not found at {self.config.CREDENTIALS_FILE}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.config.CREDENTIALS_FILE),
                    self.config.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            with open(self.config.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_summary(
        self,
        email_data: EmailData,
        create_draft: bool = False
    ) -> dict:
        """
        Send or create draft of lesson summary email
        Returns dict with 'id', 'status', 'threadId'
        """
        message = self._create_message(email_data)

        try:
            if create_draft or not self.config.AUTO_SEND_EMAIL:
                return self._create_draft(message)
            else:
                return self._send_message(message)

        except HttpError as error:
            print(f'Gmail API error: {error}')
            raise

    def _create_message(self, email_data: EmailData) -> dict:
        """Create email message with HTML formatting"""
        message = MIMEMultipart('alternative')
        message['Subject'] = email_data.subject
        message['From'] = self.config.GMAIL_SENDER_EMAIL
        message['To'] = email_data.to_email

        # Plain text version
        text_body = self._format_text_body(email_data)
        text_part = MIMEText(text_body, 'plain')

        # HTML version
        html_body = self._format_html_body(email_data)
        html_part = MIMEText(html_body, 'html')

        # Attach both versions (email clients will show HTML if supported)
        message.attach(text_part)
        message.attach(html_part)

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    def _format_text_body(self, email_data: EmailData) -> str:
        """Format plain text email body"""
        summary = email_data.summary

        body = f"""Hi {email_data.student_name},

Great class today! Here's what we covered:

📚 WHAT WE COVERED TODAY
"""
        for i, topic in enumerate(summary.covered_topics, 1):
            body += f"{i}. {topic}\n"

        body += "\n🔑 KEY VOCABULARY\n"
        for term, definition in summary.key_vocabulary.items():
            body += f"• {term}: {definition}\n"

        body += f"\n🌟 YOUR PROGRESS\n{summary.progress_note}\n"

        body += "\n📝 PRACTICE SUGGESTIONS\n"
        for i, task in enumerate(summary.homework, 1):
            body += f"{i}. {task}\n"

        if email_data.slide_link:
            body += f"\n📎 CLASS MATERIALS\nView/Download: {email_data.slide_link}\n"

        body += f"\nLooking forward to our next session!\n\nBest regards,\n{email_data.sender_name}"

        return body

    def _format_html_body(self, email_data: EmailData) -> str:
        """Format HTML email body"""
        summary = email_data.summary

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }}
        .section {{
            margin-bottom: 25px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section-title {{
            color: #667eea;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        .section-title::before {{
            content: "";
            display: inline-block;
            width: 4px;
            height: 20px;
            background: #667eea;
            margin-right: 10px;
            border-radius: 2px;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        li:last-child {{
            border-bottom: none;
        }}
        .vocab-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .vocab-table td {{
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        .vocab-table td:first-child {{
            font-weight: bold;
            color: #667eea;
            width: 30%;
        }}
        .progress-note {{
            background: #e8f5e9;
            padding: 15px;
            border-left: 4px solid #4caf50;
            border-radius: 4px;
            font-style: italic;
        }}
        .cta-button {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            margin-top: 10px;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Your Lesson Summary 📚</h1>
        <p>{email_data.lesson_date}</p>
    </div>

    <div class="content">
        <p>Hi {email_data.student_name},</p>
        <p>Great class today! Here's what we covered:</p>

        <div class="section">
            <div class="section-title">What We Covered Today</div>
            <ul>
"""

        for topic in summary.covered_topics:
            html += f"                <li>✓ {topic}</li>\n"

        html += """            </ul>
        </div>

        <div class="section">
            <div class="section-title">Key Vocabulary</div>
            <table class="vocab-table">
"""

        for term, definition in summary.key_vocabulary.items():
            html += f"""                <tr>
                    <td>{term}</td>
                    <td>{definition}</td>
                </tr>
"""

        html += """            </table>
        </div>

        <div class="section">
            <div class="section-title">Your Progress</div>
            <div class="progress-note">
"""
        html += f"                {summary.progress_note}\n"
        html += """            </div>
        </div>

        <div class="section">
            <div class="section-title">Practice Suggestions</div>
            <ul>
"""

        for task in summary.homework:
            html += f"                <li>📝 {task}</li>\n"

        html += """            </ul>
        </div>
"""

        if email_data.slide_link:
            html += f"""
        <div class="section">
            <div class="section-title">Class Materials</div>
            <p>Access your lesson slides and materials:</p>
            <a href="{email_data.slide_link}" class="cta-button">View Slides</a>
        </div>
"""

        html += f"""
        <div class="footer">
            <p>Looking forward to our next session!</p>
            <p><strong>{email_data.sender_name}</strong></p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def _send_message(self, message: dict) -> dict:
        """Send email message"""
        sent_message = self.service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        return {
            'id': sent_message['id'],
            'status': 'sent',
            'threadId': sent_message.get('threadId')
        }

    def _create_draft(self, message: dict) -> dict:
        """Create email draft"""
        draft = self.service.users().drafts().create(
            userId='me',
            body={'message': message}
        ).execute()

        return {
            'id': draft['id'],
            'status': 'draft',
            'messageId': draft['message']['id']
        }

    def get_draft_url(self, draft_id: str) -> str:
        """Get URL to view draft in Gmail"""
        return f"https://mail.google.com/mail/u/0/#drafts/{draft_id}"


def create_email_data(
    student_email: str,
    student_name: str,
    summary: LessonSummary,
    lesson_date: str,
    slide_link: Optional[str] = None,
    sender_name: str = "Your Tutor"
) -> EmailData:
    """Helper function to create EmailData object"""

    # Create subject line from first covered topic
    main_topic = summary.covered_topics[0] if summary.covered_topics else "Today's Lesson"
    subject = f"Your Lesson Summary - {main_topic}"

    return EmailData(
        to_email=student_email,
        student_name=student_name,
        subject=subject,
        summary=summary,
        slide_link=slide_link,
        lesson_date=lesson_date,
        sender_name=sender_name
    )
