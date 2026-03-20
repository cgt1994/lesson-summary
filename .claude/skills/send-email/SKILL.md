---
name: send-email
description: Generates a professional email draft from text content using the current model, then opens it in Gmail.
argument-hint: [input-file] [--type TYPE] [--to RECIPIENT] [--subject SUBJECT]
disable-model-invocation: false
allowed-tools: Read, Write, Bash
---

# Send Email Skill

This skill generates a professional email draft from text content (like transcripts or notes) using the current model, saves it to a file, and then opens it in Gmail via Chrome.

## Usage

```bash
/send-email <input_file> --type lesson --to "Student Name"
```

## Prompt

You are an expert email drafter.

1.  **Read the input file**: `{{$1}}`
2.  **Generate an email draft** based on the content.
    *   **Recipient**: `{{to}}` (default: "Student")
    *   **Type**: `{{type}}` (default: "lesson")
    *   **Subject**: `{{subject}}` (if not provided, generate a suitable subject)
    *   **Tone**: Professional, encouraging, and clear.
    *   **Style Guide**: If type is "lesson", follow Peggy's Bilingual Teaching Assistant style (Traditional Chinese narrative + English terms).
3.  **Save the email content** to a new file named `{{$1}}_email.txt`.
4.  **Open the draft** by running:
    ```bash
    python3 .claude/skills/send-email/scripts/send_email.py "{{$1}}_email.txt" --subject "Generated Subject"
    ```
5.  **Output** a confirmation message.
