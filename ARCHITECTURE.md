# Project Overview

## Lesson Summary Agent - Complete Python Implementation

A production-ready AI agent that automates your post-class workflow by generating personalized lesson summaries and emailing them to students.

---

## 📁 Project Structure

```
lesson-summary-agent/
│
├── 📄 README.md                    # Main documentation
├── 📄 SETUP.md                     # Detailed setup guide
├── 📄 QUICKSTART.md                # Quick reference
├── 📄 LICENSE                      # MIT License
├── 📄 .gitignore                   # Git ignore rules
├── 📄 .env.example                 # Environment template
├── 📄 requirements.txt             # Python dependencies
├── 🔧 setup.sh                     # Automated setup script
├── 🔧 run.sh                       # Quick run script
│
├── src/                            # Source code
│   ├── __init__.py                 # Package initialization
│   ├── config.py                   # Configuration management
│   ├── models.py                   # Pydantic data models
│   ├── transcript_processor.py     # Load & parse transcripts
│   ├── summarizer.py               # AI summarization (LangChain)
│   ├── drive_client.py             # Google Drive integration
│   ├── gmail_client.py             # Gmail email sending
│   ├── agent.py                    # Main orchestrator
│   ├── cli.py                      # Command-line interface
│   └── web_interface.py            # Gradio web app
│
├── transcripts/                    # Your lesson transcripts
│   └── 2026-01-07_JohnDoe_PresentPerfectTense.txt
│
├── students.json                   # Student database
├── credentials.json                # Google OAuth (you provide)
└── token.json                      # Auto-generated after auth
```

---

## 🔄 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LESSON SUMMARY AGENT                        │
└─────────────────────────────────────────────────────────────────┘

    INPUT                   PROCESSING                  OUTPUT

┌──────────┐           ┌──────────────┐           ┌──────────┐
│Transcript│──────────▶│  Transcript  │           │          │
│   File   │           │  Processor   │           │          │
└──────────┘           └──────┬───────┘           │          │
                              │                   │          │
┌──────────┐                  ▼                   │          │
│Fireflies │           ┌──────────────┐           │          │
│   API    │──────────▶│      AI      │           │  Gmail   │
└──────────┘           │ Summarizer   │──────────▶│  Email   │
                       │  (LangChain) │           │  Sender  │
                       └──────┬───────┘           │          │
                              │                   │          │
┌──────────┐                  ▼                   │          │
│  Google  │           ┌──────────────┐           │          │
│  Drive   │──────────▶│    Slide     │           │          │
│  (Slides)│           │  Retriever   │           │          │
└──────────┘           └──────────────┘           └──────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   Student    │
                       │   Database   │
                       └──────────────┘

INTERFACES:
┌─────────────┐         ┌─────────────┐
│     CLI     │         │     Web     │
│  (Click)    │         │  (Gradio)   │
└─────────────┘         └─────────────┘
```

---

## 🎯 Key Features

### 1. Transcript Processing
- **Local Files**: Support for .txt, .docx, .pdf
- **Fireflies Integration**: Direct API access to meeting transcripts
- **Smart Parsing**: Extracts student name, date, topic from filename
- **Flexible Formats**: Multiple filename patterns supported

### 2. AI Summarization
- **Multiple LLM Support**: Google Gemini or Anthropic Claude
- **Structured Output**: Pydantic models ensure consistent format
- **Customizable Prompts**: Easy to adjust to your teaching style
- **Fallback Parsing**: Handles edge cases gracefully

### 3. Google Drive Integration
- **Smart Search**: Multiple search strategies to find slides
- **Fuzzy Matching**: Finds slides even with slight name variations
- **Date-based Fallback**: Searches by date if exact match not found
- **Folder Organization**: Search within specific Drive folders

### 4. Gmail Email Sending
- **Beautiful HTML Emails**: Professional, responsive design
- **Plain Text Fallback**: Works with all email clients
- **Draft Mode**: Review before sending
- **Auto-send Option**: Fully automated workflow

### 5. Student Management
- **JSON Database**: Simple, easy to edit
- **Multiple Students**: Unlimited student profiles
- **Level Tracking**: Beginner, Intermediate, Advanced
- **Notes Field**: Custom information per student

### 6. Dual Interface
- **CLI**: Fast, scriptable, automatable
- **Web UI**: User-friendly, drag-and-drop
- **Flexible**: Use whichever fits your workflow

---

## 🚀 Quick Start

```bash
# 1. Run setup
./setup.sh

# 2. Configure
nano .env  # Add API keys

# 3. Authenticate
python -m src.cli setup

# 4. Process a lesson
./run.sh process transcripts/2026-01-07_JohnDoe_PresentPerfectTense.txt

# OR launch web interface
./run.sh web
```

---

## 📊 Module Breakdown

### config.py (Configuration)
- Environment variable loading
- Path management
- Validation logic
- Directory setup

### models.py (Data Models)
```python
- LessonSummary      # AI output structure
- TranscriptData     # Lesson information
- StudentInfo        # Student details
- EmailData          # Email composition
```

### transcript_processor.py (Input Handler)
- File loading and parsing
- Filename pattern matching
- Fireflies API integration
- Student database queries

### summarizer.py (AI Engine)
- LLM initialization (Gemini/Claude)
- Prompt engineering
- Structured output parsing
- Fallback strategies

### drive_client.py (Slide Retrieval)
- Google Drive API authentication
- Multi-strategy search algorithms
- Date-proximity matching
- Folder management

### gmail_client.py (Email Sender)
- Gmail API authentication
- HTML email templating
- Draft creation
- Send functionality

### agent.py (Orchestrator)
- Main workflow coordination
- Error handling
- Status reporting
- Preview mode

### cli.py (Command-Line)
- Click-based CLI framework
- Rich console output
- Multiple commands
- Interactive setup wizard

### web_interface.py (Web UI)
- Gradio-based interface
- File upload handling
- Real-time feedback
- Preview functionality

---

## 🔐 Security Features

- ✅ Sensitive files in .gitignore
- ✅ OAuth 2.0 for Google APIs (not service accounts)
- ✅ Environment-based secrets (.env)
- ✅ Token refresh handling
- ✅ Scope limitation (only required permissions)
- ✅ Local processing (no data sent to third parties except AI APIs)

---

## 💡 Use Cases

### Daily Workflow
1. Teach lesson on AmazingTalker
2. Save transcript to `transcripts/` folder
3. Run: `./run.sh process transcripts/file.txt`
4. Review draft in Gmail
5. Send to student

### Batch Processing
```bash
for file in transcripts/*.txt; do
    ./run.sh process "$file"
done
```

### Testing New Prompts
```bash
./run.sh preview transcripts/file.txt
# Adjust prompt in src/summarizer.py
./run.sh preview transcripts/file.txt
# Repeat until satisfied
```

---

## 📈 Performance & Costs

### Processing Time
- **Transcript loading**: <1 second
- **AI summarization**: 3-5 seconds
- **Slide search**: 1-2 seconds
- **Email creation**: <1 second
- **Total**: ~5-10 seconds per lesson

### API Costs (per lesson)
- **Google Gemini 1.5 Pro**: ~$0.02 (FREE tier: 1500 requests/day!)
- **Claude 3.5 Sonnet**: ~$0.10
- **Google Workspace APIs**: FREE
- **Monthly (20 lessons)**: $0.50 - $2.00

### Scalability
- Can process 100+ lessons/day
- No performance degradation
- Rate limits: Follow API provider limits

---

## 🛠️ Customization Points

### Change AI Model
Edit `.env`:
```bash
AI_MODEL=gemini-1.5-pro
# OR
AI_MODEL=claude-3-5-sonnet-20241022
```

### Modify Email Template
Edit `src/gmail_client.py`:
- Method: `_format_html_body()`
- Customize colors, layout, content

### Adjust AI Prompt
Edit `src/summarizer.py`:
- Method: `_create_prompt()`
- Add instructions, change tone

### Change Summary Structure
Edit `src/models.py`:
- Class: `LessonSummary`
- Add/remove fields

---

## 📚 Documentation

- **README.md**: Overview and general usage
- **SETUP.md**: Detailed installation instructions
- **QUICKSTART.md**: Command reference
- **This file**: Architecture and design

---

## 🤝 Contributing

To extend functionality:

1. Add new data models in `models.py`
2. Create new processors/clients as needed
3. Update orchestrator in `agent.py`
4. Add CLI commands in `cli.py`
5. Update web UI in `web_interface.py`

---

## ✅ Testing Checklist

- [ ] Setup script runs without errors
- [ ] `.env` file configured
- [ ] Google OAuth authentication successful
- [ ] Preview command generates summary
- [ ] Draft email created in Gmail
- [ ] Slides found in Google Drive
- [ ] Full workflow completes successfully

---

## 🎓 Learning Outcomes

This project demonstrates:

- **LangChain**: LLM orchestration and structured output
- **Pydantic**: Data validation and modeling
- **Google APIs**: OAuth, Gmail, Drive integration
- **CLI Development**: Click framework, Rich formatting
- **Web Development**: Gradio interactive apps
- **Error Handling**: Graceful degradation and fallbacks
- **Configuration Management**: Environment-based settings
- **Project Structure**: Clean, maintainable Python architecture

---

## 🌟 Next Steps

After setup, you can:

1. **Automate further**: Create cron jobs for batch processing
2. **Integrate more sources**: Add Zoom, Otter.ai, etc.
3. **Enhance AI**: Add student history context to prompts
4. **Build analytics**: Track student progress over time
5. **Deploy remotely**: Use Google Cloud Functions, AWS Lambda
6. **Mobile interface**: Create a simple mobile-responsive UI

---

**Built with ❤️ for educators who want to spend less time on admin and more time teaching!**
