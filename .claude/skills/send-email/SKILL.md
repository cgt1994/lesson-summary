---
name: send-email
description: Generate professional emails from text content (transcripts, notes, summaries) and open in Mail app to send. Creates summary, follow-up, report, announcement, or lesson emails with proper formatting.
argument-hint: [input-file] [--type TYPE] [--to RECIPIENT] [--subject SUBJECT] [--language LANG]
disable-model-invocation: false
---

# Send Email from Text

Convert text content (like lesson transcripts, meeting notes, or summaries) into professional email format and open in your default mail app for sending.

## How to use this skill

Basic usage - generate and send email:
```bash
python scripts/send_email.py "$1"
```

With options:
```bash
python scripts/send_email.py "$1" --type ${2:-summary} --to "${3:-recipient}" ${4:+--subject "$4"} ${5:+--language "$5"}
```

## Parameters

- `$1` - Input text file path (required)
- `--type` - Email type: summary, followup, report, announcement (default: summary)
- `--to` - Recipient description (default: "recipient")
- `--subject` - Custom email subject
- `--language` - Output language: en or zh (auto-detect if not specified)
- `--output` - Output file path (optional)

## Email Types

**summary** - Summarize content into key points
- Overview
- Key points (3-5 bullets)
- Action items (if any)

**followup** - Follow-up email after meeting/lesson
- Thank you note
- Key takeaways
- Next steps

**report** - Detailed report format
- Executive summary
- Detailed findings
- Recommendations

**announcement** - Announcement or update
- Main message
- Important details
- Call to action

## Examples

Generate summary email:
```
/generate-email lesson-transcript.txt
```

Follow-up email for students:
```
/generate-email meeting-notes.txt --type followup --to students
```

Chinese email with custom subject:
```
/generate-email 课程记录.txt --language zh --subject "今日课程总结"
```

Report email:
```
/generate-email project-notes.txt --type report --to "team members"
```

## Workflow Integration

**Complete workflow: Video to Email**
```bash
# Step 1: Convert video to audio
/convert-to-mp3 lesson.mp4

# Step 2: Transcribe audio
/transcribe-audio lesson.mp3

# Step 3: Generate email
/generate-email lesson.txt --type summary --to students
```

## Output Format

Generated emails include:
- **Subject line** - Clear and descriptive
- **Greeting** - Appropriate for recipient
- **Body** - Well-structured with headers and bullet points
- **Key points** - Extracted from content
- **Action items** - If applicable
- **Closing** - Professional sign-off

## Language Support

- **Auto-detection**: Analyzes content to detect Chinese or English
- **Bilingual**: Works with mixed Chinese-English content
- **Manual override**: Use `--language` to force specific language

## Tips for Best Results

1. Use clean, well-formatted input text
2. Specify recipient type for appropriate tone
3. Review generated email before sending
4. Combine with transcription for audio/video content
5. Use appropriate email type for your purpose

## What to Display

After generation:
```
✓ Email generated successfully!

Subject: [Subject Line]
Type: [Email Type]
Language: [en/zh]
Word count: [Count]

[Email Preview]

Output saved to: [File Path]
```

## Use Cases

- **Teachers**: Send lesson summaries to students
- **Team Leads**: Share meeting notes
- **Managers**: Create progress reports
- **Professionals**: Follow-up emails after calls
- **Students**: Summarize study notes
