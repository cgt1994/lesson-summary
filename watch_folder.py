#!/usr/bin/env python3
"""
Folder Watcher - Automatically processes videos dropped into the Process Lessons folder
"""
import time
import os
from pathlib import Path
import subprocess

WATCH_FOLDER = Path.home() / "Desktop" / "Process Lessons"
VIDEOS_FOLDER = Path("/Users/linhsinpei/lesson-summary-agent/videos")
PROJECT_DIR = Path("/Users/linhsinpei/lesson-summary-agent")

VIDEO_EXTENSIONS = ['.mp4', '.MP4', '.m4a', '.mov', '.MOV', '.mp3']

print("👀 Watching folder:", WATCH_FOLDER)
print("Drop video files here and they'll be processed automatically!")
print("Press Ctrl+C to stop\n")

processed_files = set()

while True:
    try:
        # Check for video files
        for file_path in WATCH_FOLDER.iterdir():
            if file_path.is_file() and file_path.suffix in VIDEO_EXTENSIONS:
                if file_path.name not in processed_files:
                    print(f"\n📹 New video detected: {file_path.name}")

                    # Move to videos folder
                    dest = VIDEOS_FOLDER / file_path.name
                    print(f"   Moving to: {dest}")
                    file_path.rename(dest)

                    # Process videos
                    print("   Starting processor...")
                    os.chdir(PROJECT_DIR)
                    subprocess.run([
                        "bash", "-c",
                        "source venv/bin/activate && python auto_process_lessons.py"
                    ])

                    # Show notification
                    subprocess.run([
                        "osascript", "-e",
                        'display notification "Check Mail.app for drafts!" with title "Lesson Processing Complete"'
                    ])

                    processed_files.add(file_path.name)
                    print(f"   ✅ Done processing {file_path.name}\n")

        time.sleep(2)  # Check every 2 seconds

    except KeyboardInterrupt:
        print("\n\n👋 Stopping folder watcher. Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)
