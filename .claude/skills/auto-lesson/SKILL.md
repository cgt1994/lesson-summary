---
name: auto-lesson
description: Complete automation of the post-class workflow. Takes a video file, transcribes it, extracts structured insights using an autonomous agent, and generates a draft email.
argument-hint: [video_file] [--to STUDENT_NAME] [--model WHISPER_MODEL]
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---

# Auto Lesson Orchestrator

This skill orchestrates the entire post-class workflow by chaining together specialized skills. It converts a raw lesson video into a polished email draft with structured insights.

## Usage

```bash
/auto-lesson <path_to_video.mp4> --to "Student Name"
```

## Prompt

You are an expert orchestrator for lesson workflows.

1.  **Transcribe the video**:
    *   Run the lesson summary script to generate a transcript:
        ```bash
        python3 .claude/skills/lesson-summary/scripts/lesson_summary.py "{{$1}}" --model {{model|default:"base"}}
        ```
    *   Find the path to the generated transcript file (it should be in `tmp/`).

2.  **Extract Insights (Agentic)**:
    *   Call the autonomous insight extractor skill:
        ```bash
        /extract-insights <transcript_file>
        ```
    *   Locate the resulting JSON file (e.g., `tmp/{{$1|basename}}_insights.json`).
    *   Read the insights JSON.

3.  **Generate Email (JSON Only)**:
    *   Call the lesson email generator skill using **ONLY** the insights JSON file:
        ```bash
        /lesson <insights_json_file> --to "{{to|default:"Student"}}"
        ```
    *   **CRITICAL:** Do NOT pass the transcript file (`.txt`) to the `/lesson` command. The email must be generated purely from the JSON insights to save tokens.
    *   Locate the generated email file (e.g., `tmp/{{$1|basename}}_email.txt`).

4.  **Open Email**:
    *   Open the generated email in Gmail:
        ```bash
        python3 .claude/skills/send-email/scripts/send_email.py "tmp/{{$1|basename}}_email.txt" --subject "Lesson Recap"
        ```

5.  **Report**: Confirm that all steps are complete and list the files generated.
