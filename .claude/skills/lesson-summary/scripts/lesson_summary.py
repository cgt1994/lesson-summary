#!/usr/bin/env python3
"""
Lesson Summary Workflow
Converts MP4 to MP3, transcribes audio, and generates email summary

Usage: python lesson_summary.py <video_file> [options]
"""

import sys
import argparse
import subprocess
from pathlib import Path
import time
import shutil

def run_command(cmd, description, timeout=600000):
    """Run a shell command and return success status"""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout/1000
        )

        elapsed = time.time() - start_time

        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            print(f"\n✅ Completed in {elapsed:.1f} seconds")
            return True, elapsed
        else:
            print(f"❌ Error: {result.stderr}")
            return False, elapsed

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout after {timeout/1000} seconds")
        return False, timeout/1000
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, time.time() - start_time

def main():
    parser = argparse.ArgumentParser(
        description='Complete lesson summary workflow: MP4 → MP3 → Text → Email',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('video_file', help='Input MP4 video file')
    parser.add_argument('--model', choices=['tiny', 'base', 'small', 'medium', 'large'],
                       default='tiny', help='Whisper model for transcription (default: tiny)')
    parser.add_argument('--type', choices=['lesson', 'summary', 'followup', 'report'],
                       default='lesson', help='Email type (default: lesson)')
    parser.add_argument('--to', dest='recipient', default='student',
                       help='Email recipient name (default: student)')
    parser.add_argument('--teacher', default='Peggy',
                       help='Teacher name for lesson type (default: Peggy)')
    parser.add_argument('--subject', help='Custom email subject')
    parser.add_argument('--keep-files', action='store_true', default=True,
                       help='Keep intermediate files (default: true)')
    parser.add_argument('--output-dir', help='Output directory (default: same as input)')

    args = parser.parse_args()

    # Validate input file
    video_path = Path(args.video_file)
    if not video_path.exists():
        print(f"❌ Error: Video file not found: {args.video_file}")
        sys.exit(1)

    if not video_path.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']:
        print(f"⚠️  Warning: File may not be a video: {video_path.suffix}")

    # Set output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = video_path.parent

    # Define file paths
    mp3_file = output_dir / f"{video_path.stem}.mp3"
    txt_file = output_dir / f"{video_path.stem}.txt"
    email_file = output_dir / f"{video_path.stem}_email.txt"

    # Get file size
    video_size = video_path.stat().st_size / (1024 * 1024)  # MB

    # Print workflow header
    print("\n" + "="*60)
    print("🎬 LESSON SUMMARY WORKFLOW")
    print("="*60)
    print(f"Input: {video_path.name} ({video_size:.1f} MB)")
    print(f"Model: {args.model}")
    print(f"Email type: {args.type}")
    print(f"Recipient: {args.recipient}")
    if args.type == 'lesson':
        print(f"Teacher: {args.teacher}")
    print("="*60)

    total_start = time.time()
    step_times = []

    # Step 1: Convert MP4 to MP3
    print("\n📹 STEP 1/3: Converting video to audio...")
    convert_cmd = f'ffmpeg -i "{video_path}" -vn -ar 44100 -ac 2 -b:a 192k "{mp3_file}" -y'
    success, elapsed = run_command(convert_cmd, "Converting MP4 to MP3", timeout=600000)

    if not success:
        print("\n❌ Workflow failed at Step 1")
        sys.exit(1)

    step_times.append(("Convert to MP3", elapsed))

    # Check MP3 file
    if not mp3_file.exists():
        print(f"❌ Error: MP3 file was not created: {mp3_file}")
        sys.exit(1)

    mp3_size = mp3_file.stat().st_size / (1024 * 1024)
    print(f"✓ MP3 created: {mp3_file.name} ({mp3_size:.1f} MB)")

    # Step 2: Transcribe audio to text
    print("\n🎙️ STEP 2/3: Transcribing audio to text...")

    # Get the path to the transcribe script
    transcribe_script = Path(__file__).parent.parent.parent / "transcribe-audio" / "scripts" / "faster_whisper_test.py"

    transcribe_cmd = f'python "{transcribe_script}" "{mp3_file}" --model {args.model} --output-dir "{output_dir}"'
    success, elapsed = run_command(transcribe_cmd, "Transcribing with faster-whisper", timeout=1800000)

    if not success:
        print("\n❌ Workflow failed at Step 2")
        sys.exit(1)

    step_times.append(("Transcribe audio", elapsed))

    # Check transcript file
    if not txt_file.exists():
        print(f"❌ Error: Transcript file was not created: {txt_file}")
        sys.exit(1)

    txt_size = txt_file.stat().st_size / 1024  # KB
    print(f"✓ Transcript created: {txt_file.name} ({txt_size:.1f} KB)")

    # Copy transcript to project tmp directory for review
    # Go up to project root: scripts -> lesson-summary -> skills -> .claude -> lesson-summary (root)
    project_root = Path(__file__).parent.parent.parent.parent.parent
    project_tmp_dir = project_root / "tmp"
    project_tmp_dir.mkdir(exist_ok=True)
    tmp_txt_file = project_tmp_dir / f"{video_path.stem}_transcript.txt"
    try:
        shutil.copy2(txt_file, tmp_txt_file)
        print(f"📋 Copy saved to: tmp/{tmp_txt_file.name}")
        print(f"   Full path: {tmp_txt_file}")
        print(f"   You can review and edit this file before generating the email")
    except Exception as e:
        print(f"⚠️  Warning: Could not copy to tmp: {e}")

    # Step 3: Generate email
    print("\n📧 STEP 3/3: Generating and sending email...")

    # Get the path to the send_email script
    email_script = Path(__file__).parent.parent.parent / "send-email" / "scripts" / "send_email.py"

    email_cmd = f'python "{email_script}" "{txt_file}" --type {args.type} --to "{args.recipient}"'

    if args.type == 'lesson':
        email_cmd += f' --teacher "{args.teacher}"'

    if args.subject:
        email_cmd += f' --subject "{args.subject}"'

    email_cmd += f' --output "{email_file}"'

    success, elapsed = run_command(email_cmd, "Generating email", timeout=120000)

    if not success:
        print("\n❌ Workflow failed at Step 3")
        sys.exit(1)

    step_times.append(("Generate email", elapsed))

    # Calculate total time
    total_time = time.time() - total_start

    # Print summary
    print("\n" + "="*60)
    print("✅ WORKFLOW COMPLETE!")
    print("="*60)

    print("\nFiles created:")
    print(f"📹 {mp3_file.name} ({mp3_size:.1f} MB)")
    print(f"📝 {txt_file.name} ({txt_size:.1f} KB)")
    print(f"📋 {tmp_txt_file.name} ({txt_size:.1f} KB) - Review copy in /tmp")
    if email_file.exists():
        email_size = email_file.stat().st_size / 1024
        print(f"📧 {email_file.name} ({email_size:.1f} KB)")

    print("\nProcessing time:")
    for step_name, step_time in step_times:
        print(f"  • {step_name}: {step_time:.1f}s")
    print(f"\n⏱️  Total: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")

    print("\n" + "="*60)
    print("💡 Email has been opened in Mail.app")
    print("   Review the content and send when ready!")
    print("\n💡 To regenerate email after editing transcript:")
    print(f"   /send-email {tmp_txt_file} --type {args.type} --to \"{args.recipient}\"")
    if args.type == 'lesson':
        print(f"   (Add --teacher \"{args.teacher}\" for lesson type)")
    print("="*60 + "\n")

    # Cleanup suggestion
    if not args.keep_files:
        print("\n🗑️  Cleaning up intermediate files...")
        mp3_file.unlink()
        txt_file.unlink()
        print("   Removed MP3 and TXT files")

if __name__ == '__main__':
    main()
