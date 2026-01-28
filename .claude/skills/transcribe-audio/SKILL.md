---
name: transcribe-audio
description: Convert audio files to text using faster-whisper. Supports MP3, MP4, WAV, M4A and other formats. Optimized for speed with multiple model options.
argument-hint: [input-file] [--model MODEL] [--language LANG] [--output-dir DIR]
disable-model-invocation: true
allowed-tools: Bash(python:*)
---

# Transcribe Audio to Text

Convert audio files (MP3, MP4, WAV, M4A, etc.) to text using faster-whisper (optimized Whisper implementation).

## Prerequisites

faster-whisper must be installed:

```bash
pip install -U faster-whisper
```

**Note:** FFmpeg is also required and should already be installed if you're using the convert-to-mp3 skill.

## How to use this skill

Basic usage (auto-detect language):
```bash
python scripts/faster_whisper_test.py "$1" --model tiny --output-dir "${2:-.}"
```

With language specified:
```bash
python scripts/faster_whisper_test.py "$1" --model tiny --language ${2:-auto} --output-dir "${3:-.}"
```

## Parameters

- `$1` - Input audio file path (required)
- `--model` - Model size: tiny, base, small, medium, large, large-v3 (default: tiny)
- `--language` - Source language: en, zh, ja, etc. (auto-detect if not specified)
- `--output-dir` - Output directory (defaults to same directory as input)

## Available Models

| Model | Size | Speed | Accuracy | Recommended For |
|-------|------|-------|----------|-----------------|
| **tiny** | 75MB | **Fastest** (40-60x) | Basic | Quick drafts, previews |
| **base** | 142MB | Fast (11-18x) | Good | General use, balanced |
| **small** | 466MB | Medium (8-12x) | Better | Important content |
| **medium** | 1.5GB | Slow (4-6x) | Very Good | High accuracy needed |
| **large-v3** | 3GB | Slowest (2-4x) | **Best** | Professional transcription |

## Examples

**Quick transcription (tiny model):**
```
/transcribe-audio lesson.mp3
```
Output: 53 min audio → ~1-2 minutes

**Better accuracy (base model):**
```
/transcribe-audio lesson.mp3 --model base
```
Output: 53 min audio → ~5 minutes

**Chinese content:**
```
/transcribe-audio 课程.mp3 --language zh --model base
```

**High accuracy (medium model):**
```
/transcribe-audio interview.mp3 --model medium
```
Output: 53 min audio → ~8 minutes

**Best quality (large-v3):**
```
/transcribe-audio important.mp3 --model large-v3
```
Note: First use will download 3GB model

## Language Codes

Common languages:
- `en` - English
- `zh` - Chinese (Mandarin)
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- Leave blank for auto-detection

## Speed Comparison

For a 53-minute audio file:

- **tiny**: ~80 seconds (40x real-time)
- **base**: ~280 seconds (11x real-time)
- **medium**: ~480 seconds (7x real-time)
- **large-v3**: ~800 seconds (4x real-time)

## Accuracy Tips

1. **For mixed Chinese-English**: Use auto-detection or specify primary language
2. **For noisy audio**: Use base or higher model
3. **For lectures/lessons**: base model is usually sufficient
4. **For professional work**: Use medium or large-v3

## Output Format

Generated files include:
- Plain text transcript (.txt)
- Timestamps for each segment
- Auto-detected language info
- Processing speed metrics

Example output:
```
✓ Transcription completed!

Input:  lesson.mp3 (53:28)
Output: lesson.txt (32.2 KB)
Model:  tiny
Language: Chinese (auto-detected)
Time:   80 seconds
Speed:  40x real-time
Location: /Users/ethan/Downloads/lesson.txt
```

## Workflow Integration

**Complete workflow: Video → Text → Email**
```bash
# Step 1: Convert video to audio
/convert-to-mp3 lesson.mp4

# Step 2: Transcribe audio
/transcribe-audio lesson.mp3 --model base

# Step 3: Generate summary email
/generate-email lesson.txt --type summary --to students
```

## Advanced Options

The script uses optimized parameters:
- `beam_size=1` - Faster decoding
- `best_of=1` - Single pass
- `temperature=0` - Deterministic output
- `vad_filter=true` - Remove silence
- `condition_on_previous_text=false` - Faster processing

## Model Download

Models are auto-downloaded on first use:
- Cached at: `~/.cache/huggingface/hub/`
- Only download once
- Can delete cache to free space

## Error Handling

Common issues:
- **"faster-whisper not installed"**: Run `pip install faster-whisper`
- **"FFmpeg not found"**: Install FFmpeg first
- **"Out of memory"**: Use smaller model (tiny or base)
- **"File not found"**: Check file path

## Performance Tips

1. **Start with tiny**: Test with tiny model first
2. **Upgrade if needed**: If accuracy is poor, try base or medium
3. **Batch processing**: Process multiple files in sequence
4. **Use appropriate model**: Don't use large-v3 unless necessary

## Use Cases

- **Teachers**: Transcribe lesson recordings
- **Students**: Convert lecture audio to text
- **Professionals**: Meeting transcriptions
- **Content Creators**: Video/podcast transcripts
- **Researchers**: Interview transcriptions
