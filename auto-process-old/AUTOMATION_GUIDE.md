# Automatic File Processing - No Prompts Needed!

## 🎯 Answer: NO, you don't need to prompt me every time!

## Three Ways to Process Files Automatically:

### Option 1: 🔥 Auto-Watch Mode (Fully Automatic)
**Best for: Continuous monitoring**

```bash
# Start watching for new videos (checks every 30 seconds)
python auto_watch.py

# Or run in background
nohup python auto_watch.py > watch.log 2>&1 &
```

**What it does:**
- ✅ Watches for new video files continuously
- ✅ Automatically transcribes when detected
- ✅ Logs everything to watch.log
- ✅ NO manual prompts needed!

**Then just:** Check the log and tell me which students need emails

---

### Option 2: 🤖 Run-Once Auto Processor
**Best for: Processing accumulated videos**

```bash
python auto_process_lessons.py
```

**What it does:**
- ✅ Finds all unprocessed videos
- ✅ Transcribes them all at once
- ✅ Shows summary of what was processed

**Then:** Tell me "Generate emails for all new students"

---

### Option 3: 💬 Just Tell Me "Read new file"
**Best for: When you want me involved**

Just say "read new file" and I'll:
1. Search for new videos
2. Transcribe them
3. Generate email drafts automatically

---

## 🎬 Recommended Setup

**For full automation:**

1. Start the auto-watch script once:
```bash
cd /Users/linhsinpei/lesson-summary-agent
source venv/bin/activate
nohup python auto_watch.py > watch.log 2>&1 &
```

2. Drop new video files in `videos/` folder

3. Check what was processed:
```bash
tail -20 watch.log
```

4. Tell me: "Generate emails for [student names]"

**That's it!** No more manual prompts needed.

---

## 📊 Check What's Been Processed

```bash
# See all transcripts
ls transcripts/

# See all email drafts
ls email_draft_*.txt

# See watch log
tail watch.log
```

---

## 🛑 Stop Auto-Watch

```bash
# Find the process
ps aux | grep auto_watch

# Kill it
kill [process_id]
```

---

## ✨ Summary

**You asked:** "Do I always need to give you a prompt?"

**Answer:** NO!

- Use **auto_watch.py** for continuous monitoring (no prompts ever)
- Use **auto_process_lessons.py** to batch process (run once)
- Or tell me **"read new file"** and I'll handle everything

Choose whichever fits your workflow!
