"""
transcribe_split.py

A small utility script to:
1. Take a long audio file (e.g. an MP3 lecture).
2. Split it into smaller time-based chunks (default: 20 minutes).
3. Transcribe each chunk using OpenAI's Audio API.
4. Save per-chunk transcripts and a merged transcript file.

Usage:
    python transcribe_split.py path/to/audio.mp3
    python transcribe_split.py path/to/audio.mp3 15   # 15-minute chunks

Requirements:
    - Python 3.10+
    - pip install -r requirements.txt
    - ffmpeg installed and available in PATH
    - OPENAI_API_KEY environment variable set
"""

import os
import sys
import math

from pydub import AudioSegment
from openai import OpenAI


def main() -> None:
    # --- CLI arguments ---
    if len(sys.argv) < 2:
        print("Usage: python transcribe_split.py path/to/audio.mp3 [chunk_minutes]")
        sys.exit(1)

    audio_path = os.path.abspath(sys.argv[1])

    # Chunk length in minutes (default = 20)
    if len(sys.argv) >= 3:
        try:
            chunk_minutes = int(sys.argv[2])
        except ValueError:
            print("chunk_minutes must be an integer (e.g. 20)")
            sys.exit(1)
    else:
        chunk_minutes = 20

    # --- OpenAI client via environment variable ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set.\n"
            "Please set it before running this script."
        )

    client = OpenAI(api_key=api_key)

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    folder = os.path.dirname(audio_path)
    basename = os.path.splitext(os.path.basename(audio_path))[0]

    print("Audio file:", audio_path)
    print("Output folder:", folder)

    # --- Load audio and compute duration ---
    print("\nLoading audio file...")
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    duration_min = duration_ms / 60000
    print(f"Total audio length: {duration_min:.1f} minutes")

    # --- Compute number of chunks ---
    chunk_ms = chunk_minutes * 60 * 1000
    num_chunks = math.ceil(duration_ms / chunk_ms)
    print(f"Splitting into {num_chunks} chunk(s) of ~{chunk_minutes} minutes each.\n")

    full_transcript_parts: list[str] = []

    # --- Process each chunk ---
    for i in range(num_chunks):
        part_num = i + 1
        start_ms = i * chunk_ms
        end_ms = min((i + 1) * chunk_ms, duration_ms)

        start_min = start_ms / 60000
        end_min = end_ms / 60000

        print(f"=== Part {part_num}: {start_min:.1f}–{end_min:.1f} min ===")

        # Slice audio
        chunk = audio[start_ms:end_ms]
        chunk_filename = f"{basename}_part_{part_num}.mp3"
        chunk_path = os.path.join(folder, chunk_filename)

        print(f"Exporting {chunk_filename} ...")
        chunk.export(chunk_path, format="mp3")

        # --- Transcribe with OpenAI ---
        print("Transcribing with OpenAI ...")
        with open(chunk_path, "rb") as f:
            # You can change the model if your account supports a different one
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=f,
                # Optional language hint, e.g. "he" for Hebrew:
                # language="he",
            )

        text = transcript.text

        # --- Save per-chunk transcript ---
        part_txt_filename = f"{basename}_part_{part_num}_transcript.txt"
        part_txt_path = os.path.join(folder, part_txt_filename)

        with open(part_txt_path, "w", encoding="utf-8") as out:
            out.write(text)

        print(f"Saved transcript -> {part_txt_filename}\n")

        full_transcript_parts.append(
            f"### Part {part_num} ({start_min:.1f}–{end_min:.1f} min)\n\n{text}"
        )

    # --- Save merged transcript ---
    full_path = os.path.join(folder, f"{basename}_full_transcript.txt")
    with open(full_path, "w", encoding="utf-8") as out:
        out.write("\n\n".join(full_transcript_parts))

    print("Done.")
    print("Full transcript saved to:", full_path)


if __name__ == "__main__":
    main()
