"""
Optional Gradio web interface for lesson summary agent
"""
import gradio as gr
from pathlib import Path

from .agent import LessonSummaryAgent
from .config import Config


def create_web_interface():
    """Create Gradio web interface"""

    agent = LessonSummaryAgent()
    config = Config()

    def process_transcript_file(file, student_email, sender_name, create_draft):
        """Process uploaded transcript file"""
        try:
            if file is None:
                return "⚠️ Please upload a transcript file", "", ""

            # Process the lesson
            result = agent.process_lesson(
                transcript_source=file.name,
                student_email=student_email if student_email else None,
                create_draft=create_draft,
                sender_name=sender_name
            )

            # Format output
            status_msg = f"""✅ Success!

**Student:** {result['student']}
**Email Status:** {result['email_status'].upper()}
**Email ID:** {result['email_id']}
**Slides Found:** {"Yes" if result['slides_found'] else "No"}
"""

            # Format summary
            summary = result['summary']
            summary_text = f"""## 📚 What We Covered Today
"""
            for i, topic in enumerate(summary.covered_topics, 1):
                summary_text += f"{i}. {topic}\n"

            summary_text += "\n## 🔑 Key Vocabulary\n"
            for term, definition in summary.key_vocabulary.items():
                summary_text += f"**{term}**: {definition}\n\n"

            summary_text += f"## 🌟 Progress Note\n{summary.progress_note}\n\n"

            summary_text += "## 📝 Practice Suggestions\n"
            for i, task in enumerate(summary.homework, 1):
                summary_text += f"{i}. {task}\n"

            return status_msg, summary_text, ""

        except Exception as e:
            return f"❌ Error: {str(e)}", "", ""

    def preview_transcript_file(file):
        """Preview summary without sending"""
        try:
            if file is None:
                return "⚠️ Please upload a transcript file"

            result = agent.preview_summary(file.name)

            summary = result['summary']
            transcript_data = result['transcript_data']

            output = f"""## Lesson Information
**Student:** {transcript_data.student_name}
**Date:** {transcript_data.date}
**Topic:** {transcript_data.topic}

## 📚 What We Covered Today
"""
            for i, topic in enumerate(summary.covered_topics, 1):
                output += f"{i}. {topic}\n"

            output += "\n## 🔑 Key Vocabulary\n"
            for term, definition in summary.key_vocabulary.items():
                output += f"**{term}**: {definition}\n\n"

            output += f"## 🌟 Progress Note\n{summary.progress_note}\n\n"

            output += "## 📝 Practice Suggestions\n"
            for i, task in enumerate(summary.homework, 1):
                output += f"{i}. {task}\n"

            return output

        except Exception as e:
            return f"❌ Error: {str(e)}"

    # Create interface
    with gr.Blocks(title="Lesson Summary Agent", theme=gr.themes.Soft()) as interface:

        gr.Markdown("""
# 📚 Lesson Summary Agent

Upload your lesson transcript and automatically generate a personalized summary email for your student.
        """)

        with gr.Tabs():

            # Tab 1: Process and Send
            with gr.Tab("Process & Send"):
                gr.Markdown("### Upload transcript and send summary email")

                with gr.Row():
                    with gr.Column():
                        file_input = gr.File(
                            label="Transcript File",
                            file_types=[".txt", ".docx", ".pdf"]
                        )
                        email_input = gr.Textbox(
                            label="Student Email (optional if in database)",
                            placeholder="student@example.com"
                        )
                        sender_input = gr.Textbox(
                            label="Sender Name",
                            value="Your Tutor"
                        )
                        draft_checkbox = gr.Checkbox(
                            label="Create Draft (don't send immediately)",
                            value=not config.AUTO_SEND_EMAIL
                        )

                        process_btn = gr.Button("Process Lesson", variant="primary")

                    with gr.Column():
                        status_output = gr.Markdown(label="Status")
                        summary_output = gr.Markdown(label="Generated Summary")

                process_btn.click(
                    fn=process_transcript_file,
                    inputs=[file_input, email_input, sender_input, draft_checkbox],
                    outputs=[status_output, summary_output, gr.Textbox(visible=False)]
                )

            # Tab 2: Preview Only
            with gr.Tab("Preview Only"):
                gr.Markdown("### Generate summary without sending (for testing)")

                with gr.Row():
                    with gr.Column():
                        preview_file_input = gr.File(
                            label="Transcript File",
                            file_types=[".txt", ".docx", ".pdf"]
                        )
                        preview_btn = gr.Button("Generate Preview", variant="secondary")

                    with gr.Column():
                        preview_output = gr.Markdown(label="Preview")

                preview_btn.click(
                    fn=preview_transcript_file,
                    inputs=[preview_file_input],
                    outputs=[preview_output]
                )

            # Tab 3: Help
            with gr.Tab("Help"):
                gr.Markdown(f"""
## How to Use

### File Format
Your transcript files should be named in this format:
```
YYYY-MM-DD_StudentName_LessonTopic.txt
```

Example: `2026-01-05_JohnDoe_GrammarLesson.txt`

### Setup Required
1. Configure API keys in `.env` file
2. Add student emails to `students.json`
3. Authenticate with Google (run `lesson-agent setup`)
4. Set your Google Drive slides folder ID

### Current Configuration
- **AI Model:** {config.AI_MODEL}
- **Sender Email:** {config.GMAIL_SENDER_EMAIL}
- **Auto Send:** {"Yes" if config.AUTO_SEND_EMAIL else "No (creates drafts)"}
- **Transcripts Folder:** {config.TRANSCRIPTS_FOLDER}

### Command Line Interface
You can also use the CLI:
```bash
lesson-agent process path/to/transcript.txt
lesson-agent preview path/to/transcript.txt
lesson-agent setup
```
                """)

        gr.Markdown("""
---
**Lesson Summary Agent v1.0** | Powered by AI
        """)

    return interface


def launch_web_app(share=False, server_port=7860):
    """Launch the Gradio web application"""
    interface = create_web_interface()
    interface.launch(share=share, server_port=server_port)


if __name__ == "__main__":
    launch_web_app()
