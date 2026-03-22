---
name: lesson-summary
description: Local media processor. Converts video to audio and transcribes it to text using local Whisper. Outputs a raw transcript file.
argument-hint: [video-file] [--model MODEL]
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---

# Lesson Summary (Local Processor)

This skill is a **purely local** media processing tool. It extracts audio from a video file and transcribes it using a local Whisper model.

**Output:** A raw transcript file (`.txt`) in the `tmp/` directory.

**Important:** This tool **DOES NOT** generate summaries, emails, or insights. It only produces the raw text transcript. Use the `/lesson` skill to process the transcript into a summary.

## Usage

```bash
/lesson-summary <path_to_video.mp4>
```

## Prompt

You are a media processing technician.

1.  **Run the transcription script**:
    ```bash
    python3 .claude/skills/lesson-summary/scripts/lesson_summary.py "{{$1}}" --model {{model|default:"base"}}
    ```

2.  **Verify Output**:
    *   Check the script output to find the path of the generated transcript file.
    *   Verify the file exists.

3.  **Report**:
    *   Confirm the transcription is complete.
    *   Output the absolute path to the generated transcript file (e.g., `tmp/video_name.txt`).
