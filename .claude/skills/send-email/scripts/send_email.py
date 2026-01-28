#!/usr/bin/env python3
"""
Generate professional emails from text content
Usage: python generate_email.py <input_file> [options]
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import os
import json
import subprocess
import urllib.parse

def detect_language(text):
    """Detect if text is primarily Chinese or English"""
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    total_chars = len(text.strip())
    return 'zh' if chinese_chars > total_chars * 0.3 else 'en'

def extract_key_points(text, max_points=5):
    """Extract key points from text"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Simple extraction - take meaningful lines
    key_points = []
    for line in lines:
        # Skip very short lines or timestamps
        if len(line) < 20 or line.startswith('['):
            continue
        # Skip if it's just a number or single word
        if len(line.split()) < 3:
            continue
        key_points.append(line)
        if len(key_points) >= max_points:
            break

    return key_points[:max_points]

def generate_summary_email(content, to_recipient, language, subject=None):
    """Generate a summary email"""

    if language == 'zh':
        greeting = f"亲爱的{to_recipient}，\n"
        intro = "以下是内容摘要：\n"
        key_points_header = "\n主要要点："
        closing = "\n此致\n敬礼"
        default_subject = "内容摘要"
    else:
        greeting = f"Dear {to_recipient},\n"
        intro = "Here's a summary of the content:\n"
        key_points_header = "\nKey Points:"
        closing = "\n\nBest regards"
        default_subject = "Content Summary"

    subject = subject or default_subject
    key_points = extract_key_points(content)

    email = f"Subject: {subject}\n\n"
    email += greeting
    email += f"\n{intro}"
    email += key_points_header

    for i, point in enumerate(key_points, 1):
        # Truncate long points
        point = point[:200] + "..." if len(point) > 200 else point
        email += f"\n{i}. {point}"

    email += f"\n{closing}\n"

    return email

def generate_followup_email(content, to_recipient, language, subject=None):
    """Generate a follow-up email"""

    if language == 'zh':
        greeting = f"亲爱的{to_recipient}，\n"
        intro = "感谢您的参与！以下是我们讨论的要点：\n"
        next_steps = "\n后续步骤："
        closing = "\n期待与您继续合作。\n\n此致\n敬礼"
        default_subject = "后续跟进"
    else:
        greeting = f"Dear {to_recipient},\n"
        intro = "Thank you for your participation! Here are the key takeaways:\n"
        next_steps = "\nNext Steps:"
        closing = "\n\nLooking forward to our continued collaboration.\n\nBest regards"
        default_subject = "Follow-up"

    subject = subject or default_subject
    key_points = extract_key_points(content, max_points=3)

    email = f"Subject: {subject}\n\n"
    email += greeting
    email += f"\n{intro}"

    for i, point in enumerate(key_points, 1):
        point = point[:150] + "..." if len(point) > 150 else point
        email += f"\n• {point}"

    email += next_steps
    email += "\n• Review the discussed materials"
    email += "\n• Prepare for the next session"

    email += f"\n{closing}\n"

    return email

def generate_report_email(content, to_recipient, language, subject=None):
    """Generate a detailed report email"""

    if language == 'zh':
        greeting = f"亲爱的{to_recipient}，\n"
        intro = "以下是详细报告：\n"
        summary_header = "\n概述："
        details_header = "\n详细信息："
        closing = "\n\n此致\n敬礼"
        default_subject = "详细报告"
    else:
        greeting = f"Dear {to_recipient},\n"
        intro = "Please find the detailed report below:\n"
        summary_header = "\nExecutive Summary:"
        details_header = "\nDetailed Information:"
        closing = "\n\nBest regards"
        default_subject = "Detailed Report"

    subject = subject or default_subject
    key_points = extract_key_points(content, max_points=7)

    email = f"Subject: {subject}\n\n"
    email += greeting
    email += f"\n{intro}"
    email += summary_header

    # Add first 2 points as summary
    for point in key_points[:2]:
        point = point[:200] + "..." if len(point) > 200 else point
        email += f"\n• {point}"

    email += details_header

    # Add remaining points as details
    for i, point in enumerate(key_points[2:], 1):
        point = point[:250] + "..." if len(point) > 250 else point
        email += f"\n\n{i}. {point}"

    email += f"\n{closing}\n"

    return email

def generate_lesson_email(content, to_recipient, language, subject=None, teacher_name="Peggy"):
    """Generate a teaching lesson summary email following Peggy's style guide

    Note: This function creates a prompt that should be processed by Claude Code's AI.
    It outputs a request for the AI to generate the email, rather than generating it directly.
    """

    # Read the style guide
    style_guide_path = Path(__file__).parent.parent.parent.parent / "templates" / "Master_EmailStyle_Guide.md"

    if style_guide_path.exists():
        with open(style_guide_path, 'r', encoding='utf-8') as f:
            style_guide = f.read()
    else:
        style_guide = "Use Peggy's teaching assistant style guide format."

    # Create the email template request
    email = f"""📧 AI GENERATION REQUEST
===========================================

Please generate a lesson summary email following this style guide:

{style_guide}

---

LESSON TRANSCRIPT:
{content[:6000]}

---

REQUIREMENTS:
1. Follow the "Narrative + Highlights" method (story with ✅ bullets)
2. Use bilingual format (Chinese narrative, English terms in Traditional Chinese)
3. Identify 2-3 main topics covered
4. Extract specific phrases, vocabulary, or grammar points
5. Include personalized encouragement based on progress
6. Avoid robotic tone - use "我們練習了" not "學生學習了"
7. Use the exact format from the template
8. Teacher name: {teacher_name}
9. End with:

附件是今天課程PPT，有問題可以隨時找我
有空也可以留一下課程評價喔～

Best regards,
{teacher_name}

===========================================
Please generate the complete email above.
"""

    return email

def generate_email(input_file, email_type='summary', to_recipient='recipient',
                  subject=None, tone='professional', output_file=None, language=None, teacher_name='Peggy'):
    """Main function to generate email"""

    # Read input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_file}")
        return None

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip():
        print(f"❌ Error: File is empty: {input_file}")
        return None

    # Detect language if not specified
    if language is None:
        language = detect_language(content)

    print(f"📧 Generating {email_type} email...")
    print(f"🌐 Language: {language}")
    print(f"👥 To: {to_recipient}")
    print()

    # Generate email based on type
    if email_type == 'summary':
        email = generate_summary_email(content, to_recipient, language, subject)
    elif email_type == 'followup':
        email = generate_followup_email(content, to_recipient, language, subject)
    elif email_type == 'report':
        email = generate_report_email(content, to_recipient, language, subject)
    elif email_type == 'announcement':
        email = generate_announcement_email(content, to_recipient, language, subject)
    elif email_type == 'lesson':
        email = generate_lesson_email(content, to_recipient, language, subject, teacher_name)
        if email is None:
            return None
    else:
        print(f"❌ Unknown email type: {email_type}")
        return None

    # Set output file
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_email.txt"
    else:
        output_file = Path(output_file)

    # Save email
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(email)

    # Display results
    print("=" * 60)
    print("✓ Email generated successfully!")
    print("=" * 60)
    print(f"\n{email}\n")
    print("=" * 60)
    print(f"📄 Output file: {output_file}")
    print(f"📊 Word count: {len(email.split())}")
    print(f"📏 Character count: {len(email)}")
    print("=" * 60)

    # Open in Mail app
    open_in_mail_app(email, subject or "Email from Transcript")

    return str(output_file)

def open_in_mail_app(email_content, subject):
    """Open the generated email in Mail.app"""

    # Extract subject if it's in the email content
    if email_content.startswith("Subject:"):
        lines = email_content.split('\n')
        subject_line = lines[0].replace("Subject:", "").strip()
        body = '\n'.join(lines[2:])  # Skip subject and empty line
    else:
        subject_line = subject
        body = email_content

    # Remove AI generation request markers if present
    if "AI GENERATION REQUEST" in body:
        # This is a lesson type that needs AI generation
        print("\n💡 Note: This email contains an AI generation request.")
        print("   Please review and generate the final email content before sending.")

    # URL encode the subject and body
    subject_encoded = urllib.parse.quote(subject_line)
    body_encoded = urllib.parse.quote(body)

    # Create mailto URL
    mailto_url = f"mailto:?subject={subject_encoded}&body={body_encoded}"

    # Open in default mail app (works on macOS)
    try:
        subprocess.run(['open', mailto_url], check=True)
        print("\n✅ Opening Mail app...")
        print("📬 A new email draft has been created with the content.")
    except Exception as e:
        print(f"\n⚠️  Could not open Mail app automatically: {e}")
        print("📋 Email content has been saved to file. You can copy it manually.")

def main():
    parser = argparse.ArgumentParser(
        description='Generate professional emails from text content',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input_file', help='Input text file')
    parser.add_argument('--type', choices=['summary', 'followup', 'report', 'announcement', 'lesson'],
                       default='summary', help='Email type (default: summary)')
    parser.add_argument('--to', dest='to_recipient', default='recipient',
                       help='Recipient description (default: recipient)')
    parser.add_argument('--subject', help='Email subject line')
    parser.add_argument('--tone', choices=['formal', 'casual', 'friendly', 'professional'],
                       default='professional', help='Writing tone (default: professional)')
    parser.add_argument('--teacher', dest='teacher_name', default='Peggy',
                       help='Teacher name for lesson type (default: Peggy)')
    parser.add_argument('--output', dest='output_file', help='Output file path')
    parser.add_argument('--language', choices=['en', 'zh'],
                       help='Output language (auto-detect if not specified)')

    args = parser.parse_args()

    generate_email(
        args.input_file,
        email_type=args.type,
        to_recipient=args.to_recipient,
        subject=args.subject,
        tone=args.tone,
        output_file=args.output_file,
        language=args.language,
        teacher_name=args.teacher_name
    )

if __name__ == '__main__':
    main()
