---
name: extract-insights
description: Analyzes a raw lesson transcript and extracts vocabulary, concepts, and mistakes into a structured JSON format.
context: fork
agent: general-purpose
---
# Insight Extraction Task
You are an analytical sub-agent. Your goal is to read the attached transcript and extract key learning metrics.

1. Read the provided `.txt` transcript file.
2. Extract the Key Concepts, Vocabulary Taught, and Student Mistakes.
3. Review your own work: Did you miss any implicit grammar errors in the student's speech? If so, add them to your extraction.
4. Output the final result as a valid JSON object and save it to `tmp/insights.json`.
5. Terminate and return success to the main session.