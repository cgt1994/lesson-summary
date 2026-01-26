#!/usr/bin/env python3
"""
Fully Automatic Lesson Processor
Watches for new video files and automatically processes them:
1. Transcribes with Whisper
2. Generates email draft using Claude API

Usage:
    python auto_process_lessons.py

This will process any new mp4/m4a/mov/mp3 files in the videos/ folder.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import whisper
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment
load_dotenv()

def find_unprocessed_videos():
    """Find video files that haven't been transcribed yet"""
    # Search for video files
    video_extensions = ['.mp4', '.m4a', '.mov', '.mp3', '.MP4', '.MOV']
    video_paths = []

    # Check videos subdirectory
    videos_dir = Path('videos')
    if videos_dir.exists():
        for ext in video_extensions:
            video_paths.extend(videos_dir.glob(f'*{ext}'))

    # Filter out already processed ones
    transcripts_dir = Path('transcripts')
    transcripts_dir.mkdir(exist_ok=True)

    unprocessed = []
    for video_path in video_paths:
        # Extract date and student name from filename
        filename = video_path.stem

        # Check if transcript already exists (check multiple possible formats)
        import re
        match = re.match(r'([A-Za-z]+)(\d{4})', filename)
        if match:
            student_name = match.group(1)
            date_str = f"202601{match.group(2)[2:]}"
        else:
            parts = filename.split('_')
            if len(parts) > 1:
                student_name = parts[1]
                date_str = parts[0]
            else:
                student_name = filename
                date_str = datetime.now().strftime("%Y%m%d")

        transcript_path = transcripts_dir / f"{date_str}_{student_name}.txt"

        if not transcript_path.exists():
            unprocessed.append(video_path)

    return unprocessed


def transcribe_video(video_path: Path) -> tuple[Path, str]:
    """Transcribe video and return transcript path and student name"""
    print(f"\n🎥 Transcribing: {video_path}")

    # Load Whisper model
    print("   Loading Whisper model...")
    model = whisper.load_model("base")

    # Transcribe
    print("   Transcribing (this may take a few minutes)...")
    result = model.transcribe(str(video_path))
    transcript_text = result["text"]

    # Extract student name from filename
    filename = video_path.stem

    # Try different patterns
    import re

    # Pattern 1: "Name MMDD" with space (e.g., "Bill 0121", "Charlotte 0119")
    match = re.match(r'^([A-Za-z]+)\s+(\d{4})$', filename)
    if match:
        student_name = match.group(1)
        date_str = f"202601{match.group(2)[2:]}"  # Assume 2026-01-XX
    # Pattern 2: "Name_MMDD" with underscore (e.g., "Ming_0121", "John_0121")
    elif re.match(r'^([A-Za-z]+)_(\d{4})$', filename):
        match = re.match(r'^([A-Za-z]+)_(\d{4})$', filename)
        student_name = match.group(1)
        date_str = f"202601{match.group(2)[2:]}"  # Assume 2026-01-XX
    # Pattern 3: "NameMMDD" no space (e.g., "Ariel0114", "May0114")
    elif re.match(r'^([A-Za-z]+)(\d{4})$', filename):
        match = re.match(r'^([A-Za-z]+)(\d{4})$', filename)
        student_name = match.group(1)
        date_str = f"202601{match.group(2)[2:]}"  # Assume 2026-01-XX
    # Pattern 4: "YYYYMMDD_Name" (e.g., "20260119_Charlotte")
    elif '_' in filename and re.match(r'^\d{8}_', filename):
        parts = filename.split('_')
        student_name = parts[1]
        date_str = parts[0]
    # Pattern 5: Just name (no date)
    else:
        student_name = re.sub(r'[_\d\s]+', '', filename).strip()  # Remove numbers, underscores, spaces
        date_str = datetime.now().strftime("%Y%m%d")

    # Save transcript
    transcripts_dir = Path('transcripts')
    transcripts_dir.mkdir(exist_ok=True)
    transcript_path = transcripts_dir / f"{date_str}_{student_name}.txt"

    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript_text)

    print(f"   ✅ Transcript saved: {transcript_path}")
    print(f"   📊 Length: {len(transcript_text)} characters")

    return transcript_path, student_name


def generate_email_with_claude(transcript_path: Path, student_name: str) -> Path:
    """Generate email draft using Claude API"""
    print(f"\n📧 Generating email for {student_name}...")

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in .env file.\n"
            "Please add it: ANTHROPIC_API_KEY=your_key_here\n"
            "Get one at: https://console.anthropic.com/"
        )

    # Read transcript
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    # Read style guide
    style_guide_path = Path('templates/Master_EmailStyle_Guide.md')
    with open(style_guide_path, 'r', encoding='utf-8') as f:
        style_guide = f.read()

    # Initialize Claude
    client = Anthropic(api_key=api_key)

    # Create prompt
    prompt = f"""You are Peggy's Executive Teaching Assistant. Generate an email summary for the student following the style guide exactly.

STYLE GUIDE:
{style_guide}

TRANSCRIPT:
{transcript_text}

STUDENT NAME: {student_name}
LESSON DATE: {transcript_path.stem.split('_')[0]}

Generate the complete email following the template format. Use:
- THE VERY FIRST LINE must be "Hi {{student_name}}," with NO blank lines before it
- Do NOT include "Subject:" line in the output
- 📚 for "今天學了什麼？"
- ✅ for bullet points
- 💪🏻 for encouragement section (only if there's specific praise)
- 🏡 for homework section

Remember:
1. The first line of your output MUST be "Hi {{student_name}}," (no blank lines, no subject line)
2. Start each topic with a narrative sentence in Traditional Chinese
3. Follow with ✅ bullet points for specific learning highlights
4. Use bilingual format (Traditional Chinese + English terms)
5. Write specific encouragement about improvement, not generic praise
6. Keep it concise and focused on the story of the lesson"""

    # Call Claude API
    print("   Calling Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    email_content = message.content[0].text

    # Aggressively strip any leading blank lines or whitespace
    email_content = email_content.lstrip()

    print(f"   ✅ Email generated for {student_name}")

    return email_content


def open_mail_with_draft(student_name: str, email_content: str):
    """Open Mail.app and create a new draft with the email content"""
    import subprocess
    import tempfile

    print(f"   📬 Opening Mail.app for {student_name}...")

    # Set fixed subject line
    subject_line = "AT Lesson with Peggy"

    # Remove subject line from body if it exists in the email content
    body = email_content

    # Remove "Subject:" line if present
    if "Subject:" in body:
        # Split by lines and find where the actual content starts
        lines = body.split("\n")
        # Skip the subject line and any blank lines after it
        content_start = 0
        for i, line in enumerate(lines):
            if line.startswith("Subject:"):
                content_start = i + 1
                break
        # Skip any blank lines after subject
        while content_start < len(lines) and lines[content_start].strip() == "":
            content_start += 1
        body = "\n".join(lines[content_start:])

    # Aggressively strip ALL leading/trailing whitespace
    body = body.strip()

    # Remove any remaining leading blank lines (just to be absolutely sure)
    while body.startswith("\n"):
        body = body[1:]

    # Write body to temporary file to avoid escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(body)
        temp_file = f.name

    # AppleScript to create a new email draft in Mail.app
    applescript = f'''
    set emailBody to read (POSIX file "{temp_file}") as «class utf8»

    tell application "Mail"
        activate
        set newMessage to make new outgoing message with properties {{subject:"{subject_line}", visible:true}}
        tell newMessage
            set sender to "peggylin.english@gmail.com"
            set content to emailBody
        end tell
    end tell
    '''

    try:
        result = subprocess.run(['osascript', '-e', applescript], check=True, capture_output=True, text=True)
        print(f"   ✅ Mail.app opened with draft for {student_name}")
        if result.stderr:
            print(f"   ⚠️  AppleScript warning: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Could not open Mail.app automatically: {e}")
        print(f"   💡 stdout: {e.stdout}")
        print(f"   💡 stderr: {e.stderr}")
    finally:
        # Clean up temp file after a brief delay to ensure Mail.app has read it
        import os
        import time
        time.sleep(1)  # Give Mail.app time to process the HTML content
        try:
            os.unlink(temp_file)
        except:
            pass


def main():
    """Main entry point"""
    print("=" * 70)
    print("🤖 FULLY AUTOMATIC LESSON PROCESSOR")
    print("=" * 70)
    print("\nSearching for unprocessed video files...")

    unprocessed_videos = find_unprocessed_videos()

    if not unprocessed_videos:
        print("\n✅ No new videos to process! All caught up.")
        return

    print(f"\n📹 Found {len(unprocessed_videos)} new video(s) to process:")
    for video in unprocessed_videos:
        print(f"   • {video}")

    print("\n" + "=" * 70)

    # Process each video
    results = []
    for video_path in unprocessed_videos:
        try:
            # Step 1: Transcribe
            transcript_path, student_name = transcribe_video(video_path)

            # Step 2: Generate email
            email_content = generate_email_with_claude(transcript_path, student_name)

            # Step 3: Open Mail.app with the draft
            open_mail_with_draft(student_name, email_content)

            results.append({
                'video': video_path,
                'transcript': transcript_path,
                'student': student_name,
                'status': 'success'
            })
        except Exception as e:
            print(f"\n❌ Error processing {video_path}: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                'video': video_path,
                'status': 'failed',
                'error': str(e)
            })

    # Summary
    print("\n" + "=" * 70)
    print("📊 PROCESSING SUMMARY")
    print("=" * 70)

    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']

    print(f"\n✅ Successfully processed: {len(successful)}")
    for result in successful:
        print(f"   • {result['student']}:")
        print(f"     - Transcript: {result['transcript']}")

    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for result in failed:
            print(f"   • {result['video']}: {result['error']}")

    print("\n🎉 All done! You can now review and send the emails.")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
