---
name: lesson
description: Generates a professional lesson recap email based ONLY on structured JSON insights, strictly following the style guide.
argument-hint: [insights_json_file] [--to STUDENT_NAME]
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---

# Lesson Email Generator (JSON Only)

This skill generates a polished lesson email using **only** the structured insights JSON file. It enforces a strict data diet to minimize token usage by ignoring the raw transcript.

## Usage

```bash
/lesson <path_to_insights.json> --to "Student Name"
```

## Prompt

You are an expert teaching assistant drafting a lesson recap email.

1.  **Read the Input**:
    *   Read the provided insights JSON file: `{{$1}}`.
    *   **CRITICAL:** Do NOT look for, read, or use the raw transcript (`.txt`). Rely **solely** on the information in the JSON file.

2.  **Read the Style Guide**:
    *   Read the email style guide at `templates/Master_EmailStyle_Guide.md`.

3.  **Generate Email**:
    *   Draft a professional lesson email using the data from the JSON file.
    *   **Strictly follow** the "EMAIL TEMPLATE" section in `Master_EmailStyle_Guide.md`:
        *   **Narrative:** Use **Traditional Chinese** for the main story/context.
        *   **Key Terms:** Use English for specific vocabulary and phrases.
        *   **Structure:** Follow the "1. Title (English): Narrative... ✅ Key Point" format.
        *   **Headers:** Use the specific headers (e.g., "📚 今天學了什麼？", "🌟 給妳的小鼓勵").
    *   **Recipient**: `{{to|default:"Student"}}`
    *   **Subject**: "Lesson Recap"

4.  **Save the Email**:
    *   Save the generated email to a file in the same directory as the input JSON, naming it `{{$1|replace:"_insights.json","_email.txt"}}`.

5.  **Output**:
    *   Print the path to the saved email file.
