# Setup Guide

Complete step-by-step setup instructions for Lesson Summary Agent.

## Prerequisites

- Python 3.9 or higher
- Gmail account
- Google Cloud Platform account (free tier is sufficient)
- AI API key (Google AI Studio or Anthropic)

## Step 1: Clone/Download the Project

```bash
cd ~/lesson-summary-agent
```

## Step 2: Run the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Create necessary directories
- Generate sample files

## Step 3: Get Google AI API Key

### Option A: Google Gemini (Recommended - Free tier available)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key

### Option B: Anthropic Claude

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up for an account
3. Go to API Keys section
4. Create a new API key
5. Copy the API key

## Step 4: Configure Environment Variables

Edit the `.env` file:

```bash
nano .env
```

Add your API key:

```bash
# For Gemini:
GOOGLE_API_KEY=your_google_api_key_here
AI_MODEL=gemini-1.5-pro

# OR for Claude:
ANTHROPIC_API_KEY=your_anthropic_api_key_here
AI_MODEL=claude-3-5-sonnet-20241022

# Your Gmail address
GMAIL_SENDER_EMAIL=your.email@gmail.com

# Email behavior (true = auto-send, false = create drafts)
AUTO_SEND_EMAIL=false
```

Save and exit (Ctrl+X, then Y, then Enter).

## Step 5: Set Up Google Cloud OAuth

### 5.1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Lesson Summary Agent"
4. Click "Create"

### 5.2: Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable:
   - **Gmail API**
   - **Google Drive API**

### 5.3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: **External**
   - App name: "Lesson Summary Agent"
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"
   - Scopes: Skip this step (click "Save and Continue")
   - Test users: Add your Gmail address
   - Click "Save and Continue"
4. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "Lesson Summary Agent"
   - Click "Create"
5. Click "Download JSON"
6. Rename the downloaded file to `credentials.json`
7. Move it to your project directory:
   ```bash
   mv ~/Downloads/client_secret_*.json ~/lesson-summary-agent/credentials.json
   ```

## Step 6: Run Initial Setup

Activate the virtual environment and run setup:

```bash
source venv/bin/activate
python -m src.cli setup
```

This will:
- Validate your configuration
- Open a browser for Google OAuth authentication
- Create `token.json` (saves your authentication)
- Create sample `students.json` database
- Test API connections

**Important**: When the browser opens:
1. Sign in with your Gmail account
2. You'll see a warning "Google hasn't verified this app" - click "Advanced" → "Go to Lesson Summary Agent (unsafe)"
3. Grant permissions for Gmail and Drive access
4. You'll see "The authentication flow has completed"

## Step 7: Configure Google Drive (Optional)

To enable automatic slide retrieval:

### Option A: Use Setup Wizard

The setup wizard will ask for your slides folder name and find the ID automatically.

### Option B: Manual Configuration

1. Go to [Google Drive](https://drive.google.com)
2. Navigate to your class slides folder
3. The URL will look like: `https://drive.google.com/drive/folders/ABC123XYZ`
4. Copy the folder ID (`ABC123XYZ`)
5. Add to `.env`:
   ```bash
   SLIDES_FOLDER_ID=ABC123XYZ
   ```

## Step 8: Add Your Students

Edit `students.json`:

```bash
nano students.json
```

Add your students:

```json
{
  "students": [
    {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "level": "intermediate",
      "preferred_language": "English",
      "notes": "Focuses on business English"
    },
    {
      "name": "Maria Garcia",
      "email": "maria@example.com",
      "level": "beginner",
      "preferred_language": "Spanish",
      "notes": "Very motivated, wants to improve speaking"
    }
  ]
}
```

## Step 9: Test with Sample Transcript

A sample transcript has been created. Process it:

```bash
python -m src.cli preview transcripts/2026-01-07_JohnDoe_PresentPerfectTense.txt
```

This will show you the AI-generated summary without sending an email.

## Step 10: Process Your First Lesson

Create a transcript file with the correct naming format:

```bash
# Format: YYYY-MM-DD_StudentName_LessonTopic.txt
nano transcripts/2026-01-07_YourStudent_YourTopic.txt
```

Process it:

```bash
# This will create a draft email (if AUTO_SEND_EMAIL=false)
python -m src.cli process transcripts/2026-01-07_YourStudent_YourTopic.txt

# Or send immediately with --send flag
python -m src.cli process transcripts/2026-01-07_YourStudent_YourTopic.txt --send
```

## Alternative: Use Web Interface

Launch the web app:

```bash
python -m src.web_interface
```

Open your browser to: `http://localhost:7860`

Features:
- Drag-and-drop file upload
- Visual interface
- Preview before sending

## Troubleshooting

### "credentials.json not found"

Make sure you downloaded the OAuth credentials and placed them in the project root directory.

### "GOOGLE_API_KEY not configured"

Edit `.env` and add your API key from Google AI Studio.

### "No email found for student"

Either:
- Add the student to `students.json`, OR
- Use the `--email` flag: `python -m src.cli process transcript.txt --email student@example.com`

### "Gmail API error: insufficient permissions"

Delete `token.json` and re-run setup to re-authenticate:

```bash
rm token.json
python -m src.cli setup
```

### "Google hasn't verified this app" warning

This is normal for personal projects. Click "Advanced" → "Go to Lesson Summary Agent (unsafe)" to continue.

### Python module import errors

Make sure you're in the virtual environment:

```bash
source venv/bin/activate
```

## Optional: Fireflies.ai Integration

If you use Fireflies to record lessons:

1. Get your Fireflies API key from [Fireflies Settings](https://app.fireflies.ai/integrations/custom/fireflies-api)
2. Add to `.env`:
   ```bash
   FIREFLIES_API_KEY=your_fireflies_key_here
   ```
3. Process by meeting ID:
   ```bash
   python -m src.cli process fireflies:your_meeting_id
   ```

## Next Steps

- Add all your students to `students.json`
- Organize your class slides in Google Drive with clear naming
- Set up a workflow for saving lesson transcripts
- Customize email templates in `src/gmail_client.py`
- Adjust AI prompts in `src/summarizer.py`

## Security Reminders

- Never commit `.env`, `credentials.json`, or `token.json` to version control
- Keep your API keys secure
- The `.gitignore` file is configured to prevent accidental commits
- `students.json` contains email addresses - handle with care

## Getting Help

If you encounter issues:

1. Check this setup guide
2. Review the main README.md
3. Verify your `.env` configuration
4. Check that credentials.json is in the right place
5. Try re-running the setup wizard

## Success!

You're now ready to automate your lesson summaries!

Try:
```bash
python -m src.cli process transcripts/2026-01-07_JohnDoe_PresentPerfectTense.txt
```
