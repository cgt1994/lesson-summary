---
name: convert-to-mp3
description: Convert MP4 video files to MP3 audio format. Use when the user wants to extract audio from video files or convert video to audio.
argument-hint: [input-file] [--output OUTPUT] [--bitrate BITRATE]
disable-model-invocation: true
allowed-tools: Bash(ffmpeg:*)
---

# Convert MP4 to MP3

Extract audio from MP4 video files and save as MP3 format using FFmpeg.

## Prerequisites

FFmpeg must be installed on the system:

```bash
# Check if ffmpeg is installed
which ffmpeg || echo "FFmpeg not found. Please install it first."
```

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## How to use this skill

Convert a single file:

```bash
ffmpeg -i $0 -vn -ar 44100 -ac 2 -b:a 192k ${0%.mp4}.mp3
```

If user specifies output filename:
```bash
ffmpeg -i $0 -vn -ar 44100 -ac 2 -b:a 192k $1
```

## FFmpeg parameters explained

- `-i $0` - Input file (first argument)
- `-vn` - Disable video (audio only)
- `-ar 44100` - Audio sample rate: 44.1kHz (CD quality)
- `-ac 2` - Audio channels: 2 (stereo)
- `-b:a 192k` - Audio bitrate: 192 kbps (high quality)

## Examples

Basic conversion (auto-naming):
```
/convert-to-mp3 lesson-recording.mp4
```
Output: `lesson-recording.mp3`

Specify output filename:
```
/convert-to-mp3 lesson-recording.mp4 lesson-audio.mp3
```

Custom bitrate (320k for highest quality):
```
/convert-to-mp3 lesson-recording.mp4 lesson-audio.mp3 --bitrate 320k
```

## Batch conversion

If user wants to convert multiple files:

```bash
for file in *.mp4; do
  ffmpeg -i "$file" -vn -ar 44100 -ac 2 -b:a 192k "${file%.mp4}.mp3"
done
```

## Quality settings

Recommend appropriate bitrate based on use case:

- **128k** - Good for voice/podcasts (smaller file)
- **192k** - High quality for music/lessons (recommended)
- **256k** - Very high quality
- **320k** - Maximum MP3 quality (larger file)

## What to display

After conversion completes, show:
- Input file name and size
- Output file name and size
- Conversion time
- Audio bitrate used
- Success/error message

Example output:
```
✓ Converted successfully!

Input:  lesson-recording.mp4 (245 MB)
Output: lesson-recording.mp3 (44 MB)
Bitrate: 192 kbps
Time: 12.3 seconds
```

## Error handling

Common issues:

- **"ffmpeg: command not found"**: FFmpeg not installed
- **"No such file or directory"**: Check input file path
- **"Permission denied"**: Check file permissions
- **"Invalid codec"**: File may be corrupted

## Additional features

If user wants advanced options:

**Extract specific time range:**
```bash
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:05:00 -vn -b:a 192k output.mp3
```

**Normalize audio volume:**
```bash
ffmpeg -i input.mp4 -vn -af "volume=1.5" -b:a 192k output.mp3
```

**Mono audio (smaller file):**
```bash
ffmpeg -i input.mp4 -vn -ac 1 -b:a 128k output.mp3
```
