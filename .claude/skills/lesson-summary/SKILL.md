---
name: lesson-summary
description: Complete workflow to process lesson videos - converts MP4 to MP3 and transcribes audio to text.
argument-hint: [video-file] [--model MODEL] [--to RECIPIENT]
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---

# Lesson Summary Workflow

This skill processes lesson videos by converting them to audio and transcribing them. It then triggers the generation of a lesson email.

## Usage

```bash
/lesson-summary <path_to_video.mp4> --to "Student Name"
```

## Prompt

You are an expert teaching assistant.

1.  **Run the transcription script**:
    ```bash
    python3 .claude/skills/lesson-summary/scripts/lesson_summary.py "{{$1}}" --model {{model|default:"base"}}
    ```
    This will generate a transcript file at `tmp/{{$1|basename|replace:".mp4",".txt"}}` (approximately, verify the path from the script output).

2.  **Read the transcript**: Find the transcript file path from the previous step's output and read it.

3.  **Generate a lesson email**:
    *   Read the email style guide at `templates/Master_EmailStyle_Guide.md`.
    *   Using the transcript content and the style guide, generate a professional lesson email.
    *   **Strictly follow** the "EMAIL TEMPLATE" section in the style guide:
        *   Use **Traditional Chinese** for the main narrative.
        *   Use the specific headers (e.g., "📚 今天學了什麼？", "🌟 給妳的小鼓勵").
    *   **Recipient**: `{{to|default:"Student"}}`
    *   **Subject**: "Lesson Recap"

4.  **Save the email**: Write the generated email to a file (e.g., `tmp/{{$1|basename}}_email.txt`).

5.  **Open the email**: Open the drafted email in Gmail using:
    ```bash
    python3 .claude/skills/send-email/scripts/send_email.py "tmp/{{$1|basename}}_email.txt" --subject "Lesson Recap"
    ```

6.  **Summarize**: Confirm completion.
