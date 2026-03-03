# 🚀 Fully Automated Lesson Processing

## How It Works Now

The `auto_process_lessons.py` script now does EVERYTHING automatically:

1. ✅ Finds new videos in `videos/` folder
2. ✅ Transcribes them with Whisper
3. ✅ Generates email drafts with Claude API
4. ✅ Saves everything properly named

## How to Use

### Step 1: Add video files to the `videos/` folder
File naming format (any of these work):
- `StudentName0119.mp4` (e.g., `Charlotte0119.mp4`)
- `20260119_StudentName.mp4` (e.g., `20260119_Charlotte.mp4`)
- `StudentName.mp4` (will use today's date)

### Step 2: Run the script
```bash
cd /Users/linhsinpei/lesson-summary-agent
source venv/bin/activate
python auto_process_lessons.py
```

### Step 3: Wait for it to finish
It will:
- Transcribe each video (2-5 minutes per video)
- Generate email for each transcript (30 seconds per email)
- Show you a summary of what was processed

### Step 4: Review and send
- Check the generated emails in the project folder: `email_draft_[Name]_[Date].txt`
- Review them and send to students

## Output Files

After running, you'll have:
- `transcripts/20260119_Charlotte.txt` - The transcript
- `email_draft_Charlotte_20260119.txt` - The email draft

## Example Output

```
======================================================================
🤖 FULLY AUTOMATIC LESSON PROCESSOR
======================================================================

Searching for unprocessed video files...

📹 Found 2 new video(s) to process:
   • videos/Charlotte0119.mp4
   • videos/Leon0119.mp4

======================================================================

🎥 Transcribing: videos/Charlotte0119.mp4
   Loading Whisper model...
   Transcribing (this may take a few minutes)...
   ✅ Transcript saved: transcripts/20260119_Charlotte.txt
   📊 Length: 17049 characters

📧 Generating email for Charlotte...
   Calling Claude API...
   ✅ Email saved: email_draft_Charlotte_20260119.txt

🎥 Transcribing: videos/Leon0119.mp4
   Loading Whisper model...
   Transcribing (this may take a few minutes)...
   ✅ Transcript saved: transcripts/20260119_Leon.txt
   📊 Length: 15234 characters

📧 Generating email for Leon...
   Calling Claude API...
   ✅ Email saved: email_draft_Leon_20260119.txt

======================================================================
📊 PROCESSING SUMMARY
======================================================================

✅ Successfully processed: 2
   • Charlotte:
     - Transcript: transcripts/20260119_Charlotte.txt
     - Email: email_draft_Charlotte_20260119.txt
   • Leon:
     - Transcript: transcripts/20260119_Leon.txt
     - Email: email_draft_Leon_20260119.txt

🎉 All done! You can now review and send the emails.
======================================================================
```

## Troubleshooting

If you get an error about `ANTHROPIC_API_KEY`, check your `.env` file has:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Notes

- The script only processes NEW videos (skips already-transcribed ones)
- Uses Claude Sonnet 4 for email generation (same quality as asking me directly)
- Follows the `Master_EmailStyle_Guide.md` template exactly
- Cost: ~$0.02-0.05 per email (very cheap!)
