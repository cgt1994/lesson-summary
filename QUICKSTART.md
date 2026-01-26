# Quick Reference Guide

## Common Commands

### Basic Usage

```bash
# Activate virtual environment (always do this first!)
source venv/bin/activate

# Process a lesson (creates draft by default)
python -m src.cli process transcripts/2026-01-07_Student_Topic.txt

# Send immediately instead of draft
python -m src.cli process transcripts/file.txt --send

# Specify email if not in database
python -m src.cli process transcripts/file.txt --email student@example.com

# Preview summary without sending
python -m src.cli preview transcripts/file.txt

# List all students
python -m src.cli list-students

# List Google Drive slides
python -m src.cli list-slides

# Run setup wizard
python -m src.cli setup

# Launch web interface
python -m src.web_interface
```

### File Naming Convention

Transcripts must follow this format:
```
YYYY-MM-DD_StudentName_LessonTopic.txt
```

Examples:
- `2026-01-07_JohnDoe_Grammar.txt`
- `2026-01-07_MarySmith_ConversationPractice.txt`

### students.json Structure

```json
{
  "students": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "level": "intermediate",
      "preferred_language": "English",
      "notes": "Optional notes"
    }
  ]
}
```

## Configuration (.env)

```bash
# AI Provider (choose one)
GOOGLE_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here

# Model selection
AI_MODEL=gemini-1.5-pro
# OR
AI_MODEL=claude-3-5-sonnet-20241022

# Gmail settings
GMAIL_SENDER_EMAIL=your@gmail.com
AUTO_SEND_EMAIL=false  # false = drafts, true = auto-send

# Optional: Google Drive folder for slides
SLIDES_FOLDER_ID=your_folder_id

# Optional: Fireflies integration
FIREFLIES_API_KEY=your_fireflies_key
```

## Typical Workflow

1. **After teaching a lesson:**
   - Save transcript as: `YYYY-MM-DD_StudentName_Topic.txt`
   - Place in `transcripts/` folder

2. **Process the lesson:**
   ```bash
   source venv/bin/activate
   python -m src.cli process transcripts/your-file.txt
   ```

3. **Review the draft in Gmail:**
   - Check the generated summary
   - Make any adjustments
   - Send to student

## Keyboard Shortcuts (Web Interface)

- Drag and drop transcript files directly
- Click "Process Lesson" to generate and send
- Use "Preview Only" tab to test without sending

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Module not found | `source venv/bin/activate` |
| credentials.json missing | Download from Google Cloud Console |
| No email for student | Add to students.json or use --email flag |
| API key error | Check .env file |
| Permission error | `rm token.json` then re-run setup |
| Can't find slides | Set SLIDES_FOLDER_ID in .env |

## AI Model Comparison

| Model | Speed | Cost | Quality | Recommended For |
|-------|-------|------|---------|-----------------|
| gemini-1.5-pro | Fast | $0.02/lesson | Excellent | Most users (free tier!) |
| claude-3-5-sonnet | Medium | $0.10/lesson | Excellent | Premium quality |

## File Locations

- **Transcripts**: `transcripts/`
- **Configuration**: `.env`
- **Students**: `students.json`
- **Google Auth**: `credentials.json`, `token.json`
- **Source Code**: `src/`

## Security Checklist

- [x] .env file is gitignored
- [x] credentials.json is gitignored
- [x] token.json is gitignored
- [ ] Keep API keys secure
- [ ] Don't share credentials.json
- [ ] Review students.json privacy

## Need Help?

1. Check SETUP.md for detailed instructions
2. Check README.md for full documentation
3. Run: `python -m src.cli setup` to validate config
4. Verify .env file has correct values

## Tips & Best Practices

- **Name files consistently** - Makes searching easier
- **Use drafts first** - Set AUTO_SEND_EMAIL=false until you're confident
- **Organize Drive slides** - Use clear, searchable filenames
- **Keep student database updated** - Add new students promptly
- **Review first summaries** - AI may need prompt tuning for your style
- **Backup students.json** - It contains important email addresses

## Customization

Want to change something?

- **Email template**: Edit `src/gmail_client.py`
- **AI prompt**: Edit `src/summarizer.py`
- **Summary fields**: Edit `src/models.py`
- **CLI commands**: Edit `src/cli.py`
- **Web interface**: Edit `src/web_interface.py`

## Example Session

```bash
# Start working
cd ~/lesson-summary-agent
source venv/bin/activate

# Process today's lessons
python -m src.cli process transcripts/2026-01-07_Student1_Grammar.txt
python -m src.cli process transcripts/2026-01-07_Student2_Conversation.txt

# Check what we sent
python -m src.cli list-students

# Done!
deactivate
```
