---
name: extract-insights
description: Agentic skill to analyze lesson transcripts. Chunks long texts, extracts insights with self-review, and merges results into a validated JSON.
argument-hint: [transcript-file]
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---

# Extract Insights Agent

This skill acts as an autonomous analyst. It breaks down large transcripts, analyzes them chunk-by-chunk with a self-review loop to catch implicit errors, and consolidates the findings.

## Usage

```bash
/extract-insights <path_to_transcript.txt>
```

## Agent Workflow

You are the **Insight Analyst Agent**. Your goal is to produce a high-quality, validated JSON of lesson insights.

1.  **Chunking**:
    *   The transcript might be too long. Run the chunking script:
        ```bash
        python3 .claude/skills/extract-insights/scripts/chunk_text.py "{{$1}}" 8000
        ```
    *   This will output a list of chunk files (e.g., `..._chunk_1.txt`, `..._chunk_2.txt`). Capture these filenames.

2.  **Analysis Loop (Map)**:
    *   For **EACH** chunk file:
        a.  **Read** the chunk content.
        b.  **Analyze & Extract**: Identify Vocabulary, Key Concepts, and Student Mistakes.
        c.  **Self-Review**: Ask yourself: *"Did I miss any implicit grammar errors? Are the definitions clear?"* If yes, refine the extraction.
        d.  **Output**: Generate a JSON object for this chunk.

3.  **Consolidation (Reduce)**:
    *   **Merge** the JSON objects from all chunks into a single structure.
    *   **Deduplicate** vocabulary and concepts.
    *   **Final Validation**: Ensure the format matches the required schema.

4.  **Save**:
    *   Write the final JSON to `{{$1}}_insights.json`.

5.  **Clean Up**:
    *   Delete the temporary chunk files.

## Output Schema

```json
{
  "key_concepts": ["Concept 1", "Concept 2"],
  "vocabulary": [
    {"term": "Word", "definition": "Definition", "example": "Context"}
  ],
  "mistakes": [
    {"original": "Error", "correction": "Correction", "explanation": "Why", "type": "Grammar/Pronunciation/Usage"}
  ]
}
```
