# MCP Transcription Server Setup Guide

## Current Status ✅

Your Claude Desktop config has been updated! The MCP server is configured at:
`~/Library/Application Support/Claude/claude_desktop_config.json`

## ⚠️ Disk Space Issue

Your disk is currently **98% full** (only 314 MB available). Before installing the required packages, you need to free up space.

### Quick Disk Space Cleanup:

```bash
# 1. Empty Trash
# 2. Check for large files
du -sh ~/Downloads/* | sort -h | tail -10
du -sh ~/Library/Caches/* | sort -h | tail -10

# 3. Clean pip cache (can save GBs)
pip cache purge

# 4. Clean Homebrew cache (if using Homebrew)
brew cleanup --prune=all
```

**Target:** Free up at least 2-3 GB for Whisper and PyTorch installation.

---

## Installation Steps (Run After Freeing Disk Space)

### 1. Install Required Packages

```bash
cd /Users/linhsinpei/lesson-summary-agent
source venv/bin/activate
pip install mcp openai-whisper
```

**Note:** This will download ~150MB of packages including PyTorch (large ML library).

### 2. Test the MCP Server

```bash
python transcribe_server.py
```

You should see:
```
Loading Whisper model... please wait.
```

Press `Ctrl+C` to stop.

### 3. Restart Claude Desktop

**Important:** You MUST restart Claude Desktop for it to pick up the new MCP server.

1. Quit Claude Desktop completely (Cmd+Q)
2. Reopen Claude Desktop

### 4. Verify MCP Connection

In Claude Desktop, check the bottom toolbar for the 🔌 icon (MCP servers). You should see:
- `filesystem` (already configured)
- `lesson-transcriber` (newly added)

---

## Usage in Claude Desktop

Once configured, you can use these commands in Claude:

### Transcribe a Lesson Recording

```
Transcribe this lesson for student Claire:
/path/to/recording.mp4
Topic: Grammar Lesson
```

Claude will call the `transcribe_lesson` tool automatically.

### List Recent Transcripts

```
Show me my recent lesson transcripts
```

### Quick Transcription (No Student Tracking)

```
Transcribe this video: /path/to/video.mp4
```

---

## Available MCP Tools

### 1. `transcribe_lesson`
- **Parameters:** file_path, student_name, lesson_topic (optional)
- **Output:** Saves to `transcripts/YYYYMMDD_StudentName_Topic.txt`
- **Returns:** Transcript preview and file path

### 2. `transcribe_video`
- **Parameters:** file_path
- **Output:** Returns raw transcript text (doesn't save)
- **Use:** Quick transcription without student tracking

### 3. `list_transcripts`
- **Parameters:** None
- **Output:** List of recent transcript files
- **Use:** Browse existing transcripts

---

## File Locations

### MCP Server Code
```
/Users/linhsinpei/lesson-summary-agent/transcribe_server.py
```

### Claude Desktop Config
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Transcripts Output Directory
```
/Users/linhsinpei/lesson-summary-agent/transcripts/
```

---

## Current Configuration

Your `claude_desktop_config.json` is configured as:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/linhsinpei/lesson-summary-agent/transcripts"
      ]
    },
    "lesson-transcriber": {
      "command": "python",
      "args": [
        "/Users/linhsinpei/lesson-summary-agent/transcribe_server.py"
      ]
    }
  }
}
```

---

## Troubleshooting

### "Model not found" Error
```bash
# Whisper will auto-download models on first use
# Ensure you have internet connection and disk space
```

### "ModuleNotFoundError: No module named 'mcp'"
```bash
# Make sure you're in the venv
source venv/bin/activate
pip install mcp openai-whisper
```

### MCP Server Not Showing in Claude
1. Check config file syntax (must be valid JSON)
2. Restart Claude Desktop completely
3. Check logs: `~/Library/Logs/Claude/mcp*.log`

### Transcription is Slow
- First run downloads the Whisper model (~150MB)
- Use "base" model for speed (current setting)
- Upgrade to "small" or "medium" for better accuracy

---

## Whisper Model Options

Edit `transcribe_server.py` line 20 to change models:

```python
model = whisper.load_model("base")    # Fast, good for most use cases
# model = whisper.load_model("small")  # Better accuracy, slower
# model = whisper.load_model("medium") # Best for Mandarin/English mix
```

**Model Sizes:**
- `tiny`: 39 MB
- `base`: 74 MB (current)
- `small`: 244 MB
- `medium`: 769 MB
- `large`: 1.5 GB

---

## Integration with Lesson Summary Agent

Once transcription is complete, process the transcript with:

```bash
python -m src.cli process transcripts/20260114_Claire_Grammar.txt
```

Or in Claude Desktop, simply say:
```
Process the transcript for Claire and send the summary email
```

Claude will automatically use both the transcriber and your lesson-summary-agent!

---

## Next Steps

1. **Free up disk space** (at least 2-3 GB)
2. **Install packages:** `pip install mcp openai-whisper`
3. **Restart Claude Desktop**
4. **Test transcription** with a sample recording
5. **Enjoy automated lesson summaries!**

---

## Summary

✅ MCP server code created: `transcribe_server.py`
✅ Claude Desktop config updated
✅ Requirements.txt updated with new dependencies
⏳ Waiting for disk space to install packages
⏳ Restart Claude Desktop after installation

**Status:** Ready to install once disk space is freed up!
