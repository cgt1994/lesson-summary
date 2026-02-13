#!/usr/bin/env python3
"""
Faster Whisper transcription script
Usage: python faster_whisper_test.py <audio_file> [--model base] [--language zh]
"""

import sys
import time
from pathlib import Path
from faster_whisper import WhisperModel

def transcribe_audio(audio_path, model_size="base", language=None, output_dir=None):
    """Transcribe audio file using faster-whisper"""

    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"错误: 文件不存在 {audio_path}")
        return

    # Set output directory
    if output_dir is None:
        output_dir = audio_file.parent
    else:
        output_dir = Path(output_dir)

    output_file = output_dir / f"{audio_file.stem}.txt"

    print(f"📁 输入文件: {audio_file}")
    print(f"📝 输出文件: {output_file}")
    print(f"🤖 模型大小: {model_size}")
    print(f"🌐 语言: {language or '自动检测'}")
    print()

    # Initialize model (runs on CPU with float32 for optimal Apple Silicon performance)
    print("⏳ 加载模型...")
    start_load = time.time()
    model = WhisperModel(model_size, device="cpu", compute_type="float32")
    load_time = time.time() - start_load
    print(f"✓ 模型加载完成 ({load_time:.2f}秒)")
    print()

    # Transcribe
    print("🎙️ 开始转录...")
    start_time = time.time()

    segments, info = model.transcribe(
        str(audio_file),
        language=language,
        beam_size=1,  # 降低beam_size从5到1，速度提升30-40%
        best_of=1,  # 只取最佳结果
        temperature=0,  # 确定性输出，更快
        condition_on_previous_text=False,  # 禁用上下文依赖，速度更快
        vad_filter=True,  # Voice Activity Detection - 去除静音
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    print(f"检测到的语言: {info.language} (概率: {info.language_probability:.2f})")
    print(f"音频时长: {info.duration:.2f}秒")
    print()

    # Write transcription to file
    print("💾 保存转录文本...")
    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            text = segment.text.strip()
            f.write(text + "\n")
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {text}")

    elapsed_time = time.time() - start_time

    print()
    print("=" * 60)
    print("✓ 转录完成!")
    print(f"⏱️  处理时间: {elapsed_time:.2f}秒")
    print(f"⚡ 处理速度: {info.duration / elapsed_time:.2f}x 实时速度")
    print(f"📄 输出文件: {output_file}")
    print(f"📊 文件大小: {output_file.stat().st_size / 1024:.1f} KB")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python faster_whisper_test.py <audio_file> [--model base] [--language zh]")
        sys.exit(1)

    audio_path = sys.argv[1]
    model_size = "base"
    language = None
    output_dir = None

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model_size = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--language" and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output-dir" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    transcribe_audio(audio_path, model_size, language, output_dir)
