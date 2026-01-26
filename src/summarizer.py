"""
AI-powered lesson summarization using LangChain
"""
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

from .models import LessonSummary, TranscriptData
from .config import Config


class LessonSummarizer:
    """Generate structured lesson summaries using LLMs"""

    def __init__(self, model_name: Optional[str] = None):
        self.config = Config()
        self.model_name = model_name or self.config.AI_MODEL
        self.llm = self._initialize_llm()
        self.parser = PydanticOutputParser(pydantic_object=LessonSummary)

    def _initialize_llm(self):
        """Initialize the appropriate LLM based on configuration"""
        if self.model_name.startswith("gemini"):
            if not self.config.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not configured")

            return ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=0.7,
                google_api_key=self.config.GOOGLE_API_KEY
            )

        elif self.model_name.startswith("claude"):
            if not self.config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured")

            return ChatAnthropic(
                model=self.model_name,
                temperature=0.7,
                anthropic_api_key=self.config.ANTHROPIC_API_KEY
            )

        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    def generate_summary(self, transcript_data: TranscriptData) -> LessonSummary:
        """
        Generate a structured lesson summary from transcript data
        """
        prompt = self._create_prompt()

        chain = prompt | self.llm | self.parser

        try:
            result = chain.invoke({
                "student_name": transcript_data.student_name,
                "date": transcript_data.date,
                "topic": transcript_data.topic,
                "content": self._truncate_content(transcript_data.content),
                "student_level": transcript_data.student_level or "unknown",
                "format_instructions": self.parser.get_format_instructions()
            })

            return result

        except Exception as e:
            # Fallback: try with more lenient parsing
            print(f"Warning: Structured parsing failed, retrying... ({e})")
            return self._generate_with_fallback(transcript_data)

    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the summarization prompt template"""
        template = """You are an expert language tutor assistant with years of experience creating personalized lesson summaries.

Your task is to analyze the following lesson transcript and create a structured, encouraging summary for the student.

STUDENT INFORMATION:
- Name: {student_name}
- Level: {student_level}
- Lesson Date: {date}
- Lesson Topic: {topic}

LESSON TRANSCRIPT:
{content}

INSTRUCTIONS:
1. **Covered Topics**: Extract 3-5 main topics or concepts covered in the lesson. Be specific and actionable.

2. **Key Vocabulary**: Identify 5-10 important words, phrases, or grammar points discussed. Provide clear, student-appropriate definitions.

3. **Progress Note**: Write ONE encouraging sentence about the student's progress, participation, or improvement. Be genuine and specific if possible.

4. **Homework/Practice**: Suggest 2-3 specific, actionable practice tasks the student can do before the next lesson. Make them relevant to what was covered.

TONE GUIDELINES:
- Keep the tone warm, encouraging, and professional
- Adjust complexity based on student level
- Be specific rather than generic
- Focus on what the student CAN do, not what they can't

{format_instructions}

Generate the summary now:"""

        return ChatPromptTemplate.from_template(template)

    def _truncate_content(self, content: str, max_chars: int = 8000) -> str:
        """Truncate content if too long to fit in context window"""
        if len(content) <= max_chars:
            return content

        # Truncate but try to end at a sentence
        truncated = content[:max_chars]
        last_period = truncated.rfind('.')

        if last_period > max_chars * 0.8:  # If we can find a period in last 20%
            truncated = truncated[:last_period + 1]

        return truncated + "\n\n[Transcript truncated for length]"

    def _generate_with_fallback(self, transcript_data: TranscriptData) -> LessonSummary:
        """Fallback method with simpler parsing"""
        simple_prompt = ChatPromptTemplate.from_template("""
Create a lesson summary for {student_name} about {topic}.

Transcript excerpt:
{content}

Provide:
1. Three main topics covered (as a JSON array)
2. Five key vocabulary terms with definitions (as a JSON object)
3. One encouraging progress note (as a string)
4. Two practice suggestions (as a JSON array)

Return ONLY valid JSON matching this structure:
{{
  "covered_topics": ["topic1", "topic2", "topic3"],
  "key_vocabulary": {{"word1": "definition1", "word2": "definition2"}},
  "progress_note": "Your progress note here",
  "homework": ["task1", "task2"]
}}
""")

        chain = simple_prompt | self.llm

        response = chain.invoke({
            "student_name": transcript_data.student_name,
            "topic": transcript_data.topic,
            "content": self._truncate_content(transcript_data.content, 4000)
        })

        # Parse the response content
        import json
        import re

        # Extract JSON from response
        response_text = response.content if hasattr(response, 'content') else str(response)

        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json_data = json.loads(json_match.group(0))
            return LessonSummary(**json_data)

        # Last resort: return a basic summary
        return LessonSummary(
            covered_topics=[
                f"Discussion about {transcript_data.topic}",
                "Vocabulary practice",
                "Conversation skills"
            ],
            key_vocabulary={
                "practice": "Regular exercise to improve skills",
                "fluency": "Ability to speak smoothly and easily"
            },
            progress_note=f"Great work in today's lesson, {transcript_data.student_name}!",
            homework=[
                f"Review today's vocabulary about {transcript_data.topic}",
                "Practice using new phrases in sentences"
            ]
        )


class SummaryEnhancer:
    """Optional: Enhance summaries with additional context"""

    @staticmethod
    def add_personalization(summary: LessonSummary, student_info) -> LessonSummary:
        """Add personalized touches based on student info"""
        # Could add student-specific encouragement, learning style tips, etc.
        return summary

    @staticmethod
    def format_for_email(summary: LessonSummary) -> str:
        """Format summary as plain text for email"""
        text = "📚 WHAT WE COVERED TODAY\n"
        for i, topic in enumerate(summary.covered_topics, 1):
            text += f"{i}. {topic}\n"

        text += "\n🔑 KEY VOCABULARY\n"
        for term, definition in summary.key_vocabulary.items():
            text += f"• {term}: {definition}\n"

        text += f"\n🌟 YOUR PROGRESS\n{summary.progress_note}\n"

        text += "\n📝 PRACTICE SUGGESTIONS\n"
        for i, task in enumerate(summary.homework, 1):
            text += f"{i}. {task}\n"

        return text
