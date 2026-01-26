"""
Google Drive integration for finding class slides
"""
from typing import Optional, List, Dict
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import Config


class DriveSlideRetriever:
    """Search and retrieve class slides from Google Drive"""

    def __init__(self):
        self.config = Config()
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Drive API"""
        # Token file stores user's access and refresh tokens
        if self.config.TOKEN_FILE.exists():
            self.creds = Credentials.from_authorized_user_file(
                str(self.config.TOKEN_FILE),
                self.config.SCOPES
            )

        # If credentials are invalid or don't exist, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not self.config.CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Google credentials file not found at {self.config.CREDENTIALS_FILE}\n"
                        "Please download credentials from Google Cloud Console"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.config.CREDENTIALS_FILE),
                    self.config.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.config.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('drive', 'v3', credentials=self.creds)

    def find_slides(
        self,
        student_name: str,
        date: str,
        topic: str,
        folder_id: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """
        Find class slides matching the lesson parameters
        Returns dict with 'id', 'name', 'webViewLink', 'downloadLink'
        """
        folder_id = folder_id or self.config.SLIDES_FOLDER_ID

        # Try multiple search strategies
        strategies = [
            self._search_by_all_params,
            self._search_by_name_and_topic,
            self._search_by_date,
            self._search_by_name_only
        ]

        for strategy in strategies:
            result = strategy(student_name, date, topic, folder_id)
            if result:
                return result

        return None

    def _search_by_all_params(
        self,
        student_name: str,
        date: str,
        topic: str,
        folder_id: Optional[str]
    ) -> Optional[Dict[str, str]]:
        """Search by student name, topic, and date"""
        # Build query
        query_parts = []

        # Search in specific folder if provided
        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")

        # File name contains student name and topic
        query_parts.append(f"name contains '{student_name}'")
        query_parts.append(f"name contains '{topic}'")

        # Only look for common slide formats
        mime_types = [
            "application/pdf",
            "application/vnd.google-apps.presentation",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ]
        mime_query = " or ".join([f"mimeType='{mt}'" for mt in mime_types])
        query_parts.append(f"({mime_query})")

        query = " and ".join(query_parts)

        return self._execute_search(query, date)

    def _search_by_name_and_topic(
        self,
        student_name: str,
        date: str,
        topic: str,
        folder_id: Optional[str]
    ) -> Optional[Dict[str, str]]:
        """Search by student name and topic only"""
        query_parts = []

        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")

        query_parts.append(f"name contains '{student_name}'")
        query_parts.append(f"name contains '{topic}'")

        query = " and ".join(query_parts)
        return self._execute_search(query, date)

    def _search_by_date(
        self,
        student_name: str,
        date: str,
        topic: str,
        folder_id: Optional[str]
    ) -> Optional[Dict[str, str]]:
        """Search by date in filename"""
        query_parts = []

        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")

        # Look for date in filename (YYYY-MM-DD format)
        query_parts.append(f"name contains '{date}'")

        query = " and ".join(query_parts)
        return self._execute_search(query, date)

    def _search_by_name_only(
        self,
        student_name: str,
        date: str,
        topic: str,
        folder_id: Optional[str]
    ) -> Optional[Dict[str, str]]:
        """Last resort: search by student name only"""
        query_parts = []

        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")

        query_parts.append(f"name contains '{student_name}'")

        query = " and ".join(query_parts)
        return self._execute_search(query, date)

    def _execute_search(self, query: str, lesson_date: str) -> Optional[Dict[str, str]]:
        """Execute Drive search query and return best match"""
        try:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, webViewLink, mimeType, modifiedTime)',
                orderBy='modifiedTime desc',
                pageSize=10
            ).execute()

            files = results.get('files', [])

            if not files:
                return None

            # If multiple results, try to find best match by date proximity
            if len(files) > 1:
                best_file = self._find_closest_by_date(files, lesson_date)
            else:
                best_file = files[0]

            return {
                'id': best_file['id'],
                'name': best_file['name'],
                'webViewLink': best_file['webViewLink'],
                'downloadLink': f"https://drive.google.com/uc?export=download&id={best_file['id']}"
            }

        except HttpError as e:
            print(f"Drive API error: {e}")
            return None

    def _find_closest_by_date(self, files: List[Dict], target_date: str) -> Dict:
        """Find file with modification date closest to lesson date"""
        from datetime import datetime

        try:
            target = datetime.fromisoformat(target_date)

            closest_file = files[0]
            closest_delta = float('inf')

            for file in files:
                file_date = datetime.fromisoformat(file['modifiedTime'].replace('Z', '+00:00'))
                delta = abs((file_date - target).total_seconds())

                if delta < closest_delta:
                    closest_delta = delta
                    closest_file = file

            return closest_file

        except (ValueError, KeyError):
            # If date parsing fails, just return first file
            return files[0]

    def list_recent_files(self, folder_id: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """List recent files in the slides folder (useful for debugging)"""
        folder_id = folder_id or self.config.SLIDES_FOLDER_ID

        query = f"'{folder_id}' in parents" if folder_id else None

        try:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, webViewLink, modifiedTime)',
                orderBy='modifiedTime desc',
                pageSize=limit
            ).execute()

            return results.get('files', [])

        except HttpError as e:
            print(f"Drive API error: {e}")
            return []

    def get_folder_id_by_name(self, folder_name: str) -> Optional[str]:
        """Find folder ID by name (helper for setup)"""
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"

            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()

            files = results.get('files', [])
            return files[0]['id'] if files else None

        except HttpError as e:
            print(f"Drive API error: {e}")
            return None
