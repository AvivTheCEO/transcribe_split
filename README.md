# Audio Transcriber – Split & Transcribe Long Audio Files with OpenAI

This is a small Python utility that:

1. Takes a long audio file (e.g. a 1-hour MP3).
2. Splits it into smaller chunks (default: 20 minutes per chunk).
3. Sends each chunk to OpenAI's Audio API for transcription.
4. Saves:
   - A transcript file per chunk.
   - A single merged transcript file with all chunks combined.

It is designed to work with long lectures, talks, or podcasts that might exceed common API file size limits.

---

## Features

- Split long audio files into equal time-based chunks.
- Use OpenAI's `gpt-4o-mini-transcribe` (or other supported models) to transcribe audio.
- Save:
  - `<basename>_part_X.mp3` – audio chunks
  - `<basename>_part_X_transcript.txt` – per-chunk transcripts
  - `<basename>_full_transcript.txt` – combined transcript

---

## Requirements

- Python 3.10+
- `ffmpeg` installed and available in your PATH (for `pydub` to handle audio).
- An OpenAI API key (separate from ChatGPT Plus – you need a Platform API key).

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Install ffmpeg (Windows examples)

You can install ffmpeg in several ways, for example:

- Download a static build from the official site: https://ffmpeg.org/download.html  
  Extract it and add `ffmpeg/bin` to your PATH.

or

- Using Chocolatey (as Administrator):

```bash
choco install ffmpeg -y
```

Then verify:

```bash
ffmpeg -version
```

---

## OpenAI API Key

Set your API key via environment variable:

**PowerShell (Windows):**

```powershell
$env:OPENAI_API_KEY="sk-your-real-key-here"
```

**Bash (macOS / Linux / WSL):**

```bash
export OPENAI_API_KEY="sk-your-real-key-here"
```

> 🔒 Do **not** commit your API key into git. Keep it in environment variables or a local `.env` that is ignored by git.

---

## Usage

Basic usage:

```bash
python transcribe_split.py path/to/audio.mp3
```

This will:

- Split into 20-minute chunks (default).
- Transcribe each chunk.
- Save transcripts in the same folder as the input audio.

Specify a custom chunk length (in minutes):

```bash
python transcribe_split.py path/to/audio.mp3 15
```

This will split the file into 15-minute chunks instead of 20.

---

## Outputs

Given an input file like:

```text
C:\Users\You\Desktop\lecture.mp3
```

You’ll get in the same folder:

- `lecture_part_1.mp3`
- `lecture_part_2.mp3`
- `lecture_part_3.mp3`
- `lecture_part_1_transcript.txt`
- `lecture_part_2_transcript.txt`
- `lecture_part_3_transcript.txt`
- `lecture_full_transcript.txt` (all parts merged, with headings)

---

## Notes

- The script uses `gpt-4o-mini-transcribe` by default. You can change the model name in `transcribe_split.py` if your account supports a different transcription model.
- You can optionally set a language hint (e.g. `"he"` for Hebrew) by editing the script.
- Make sure you have sufficient quota on your OpenAI account, or you will receive an `insufficient_quota` / `429` error.

---

## License

This project is released under the MIT License. See [LICENSE](./LICENSE) for details.
