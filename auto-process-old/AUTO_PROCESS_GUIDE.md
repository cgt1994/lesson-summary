# Automatic Lesson Processing

## ✅ What I Created

**`auto_process_lessons.py`** - Automatically finds and transcribes new video files.

## 📖 How It Works

The script:
1. **Searches** for video files (*.mp4, *.m4a, *.mov, *.mp3) in current directory and `videos/` folder
2. **Checks** which ones haven't been transcribed yet
3. **Transcribes** new videos using Whisper
4. **Saves** transcripts to `transcripts/` folder
5. **Reports** what it found and processed

## 🚀 Usage

### Option 1: Run the script manually
```bash
source venv/bin/activate
python3 auto_process_lessons.py
```

### Option 2: Just tell me "Read new file"
I'll automatically:
1. Search for new video files
2. Transcribe them
3. Generate email drafts for each student

## 💡 What Happens

**Before:**
- You have: `videos/NewStudent0115.mp4`

**After running:**
- Transcript created: `transcripts/20260115_NewStudent.txt`
- Then you tell me: "Generate email for NewStudent"
- Email created: `email_draft_NewStudent_20260115.txt`

## 🎯 Benefits

- ✅ No need to manually specify each video
- ✅ Automatically detects new files
- ✅ Won't re-process already transcribed videos
- ✅ Works with any filename format

## 📝 Note

The script only does **transcription** automatically. For email generation, you still need to ask me (Claude) because:
- I can analyze the transcript contextually
- I follow your Master_EmailStyle_Guide.md perfectly
- I don't need an API key (I AM Claude!)

## Example Workflow

1. Drop new video files in `videos/` folder
2. Run: `python3 auto_process_lessons.py`
3. Tell me: "Generate emails for all new transcripts"
4. Done! ✅

---

**Location:** `/Users/linhsinpei/lesson-summary-agent/auto_process_lessons.py`
