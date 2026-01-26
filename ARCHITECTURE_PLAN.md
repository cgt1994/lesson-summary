# FUTURE SPECIFICATION: Fully Automated Agent (V2)

## 1. RELATIONSHIPS
* **Parent Persona:** Inherits strict voice/tone from `Master_EmailStyle_Guide.md`.
* **Target Platform:** Gmail API (Future Integration).

## 2. INPUT LOGIC
The Agent must accept a raw file (`Current_Lesson.txt`) and perform "Pre-Processing" to generate the following metadata:
* **Student Mood:** (Inferred from transcript sentiment).
* **Class Topic:** (Extracted from file headers or keywords).

## 3. PROCESSING LOGIC (The "Playbook")

### Step 1: Categorization (New Feature)
**Action:** Parse the messy transcript.
**Transformation Rules:**
* **Vocabulary:** Extract word + CEFR definition.
* **Grammar:** Format as "You said: [X] -> Better way: [Y]".
* **Pronunciation:** Provide phonetic breakdown (e.g., "KUM-fuh-tuh-buhl").

### Step 2: Synthesis & Style
**Action:** Draft the content.
**Constraint:** Must apply the "Loop" template found in `Master_EmailStyle_Guide.md`.

## 4. OUTPUT TARGET (JSON)
*Note: This JSON output is designed for the future Python/Zapier script. Do not use for manual copy-paste.*

```json
{
  "gmail_draft": {
    "to": "{{STUDENT_EMAIL}}",
    "subject": "Great job today! 🌟 Notes on {{class_topic}}",
    "body_content": "[Rendered Email Body based on Master_Teaching_Guide.md]"
  }
}

# Output 
Refer to /Users/linhsinpei/lesson-summary-agent/templates/Master_EmailStyle_Guide.md for output.