# Simple Lesson Processing Script

## What I Created

`process_lesson_simple.py` - An end-to-end script that automatically:

1. **Transcribes** video/audio files using Whisper
2. **Generates** AI-powered email summaries using your chosen AI (Gemini or Claude)
3. **Saves** email drafts following your Master_EmailStyle_Guide.md format

## No Google Credentials Required!

Unlike the original application, this script:
- ✅ Does NOT require Google Cloud credentials
- ✅ Does NOT need Gmail API setup
- ✅ Does NOT need Google Drive API
- ✅ Only needs an AI API key (Gemini or Anthropic)

## How to Use

### Option 1: Process a video file (transcribe + email)
```bash
source venv/bin/activate
python3 process_lesson_simple.py 20260114May.mp4
```

### Option 2: Process existing transcript (email only)
```bash
source venv/bin/activate
python3 process_lesson_simple.py transcripts/20260114_May.txt
```

## Setup Required

You need ONE of these API keys in your `.env` file:

**Option A: Google Gemini (Free tier available)**
```bash
GOOGLE_API_KEY=your_actual_key_here
AI_MODEL=gemini-1.5-pro
```
Get free key at: https://makersuite.google.com/app/apikey

**Option B: Anthropic Claude**
```bash
ANTHROPIC_API_KEY=your_actual_key_here
AI_MODEL=claude-3-5-sonnet-20241022
```
Get key at: https://console.anthropic.com/

## Output

The script creates:
1. `transcripts/YYYYMMDD_StudentName.txt` - The transcript
2. `email_draft_StudentName_YYYYMMDD.txt` - The email draft in Peggy's style

## File Location

**Script:** `/Users/linhsinpei/lesson-summary-agent/process_lesson_simple.py`

## Next Steps

1. Update your `.env` file with a real API key
2. Run the script on a video or transcript
3. Copy the email draft and send it to your student!
