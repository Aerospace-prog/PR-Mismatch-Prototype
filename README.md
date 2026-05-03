#  Lightweight Audio-Subtitle Mismatch Detection Tool

> **Planet Read × C4GT (Code for Good Tech)**
> Phase 2 — Transcription & OCR Pipeline Prototype

---

##  Project Overview

This project is a **proof-of-concept AI pipeline** that extracts audio from video files, transcribes the speech using OpenAI's Whisper, extracts subtitle text via Tesseract OCR, and outputs timestamped text segments as structured JSON.

It is the **second phase** of a larger system that will automatically detect mismatches between spoken audio and on-screen subtitles — helping accessibility teams at **Planet Read** reduce manual quality-assurance effort.

---

##  Demo

[![Google Drive](https://img.shields.io/badge/Google%20Drive-Project%20Demo-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1n88v3aEXKh24p5u_fut_WJyBLKWe_fXq/view?usp=sharing)

*Click the badge above to watch the Phase 1 Pipeline Demo.*

*In this demo, the pipeline extracts audio from a sample video, runs Whisper STT, and generates a structured JSON output.*

---

##  Problem Context

[Planet Read](https://www.planetread.org/) creates Same-Language Subtitling (SLS) for media content to promote literacy across India. Ensuring that subtitles **accurately match** the spoken audio is critical for accessibility and learning outcomes.

Currently, this verification is done **manually** — a slow, error-prone process. This tool aims to **automate mismatch detection** by:

1. Transcribing the spoken audio
2. Extracting hardcoded subtitles via OCR
3. Comparing the two and flagging segments where they diverge

---

## ⚙️ Pipeline

```text
Video (.mp4)
      │
      ├──▶ Extract Audio (FFmpeg → .wav) ──▶ Transcribe (Whisper) ─┐
      │                                                            │
      │                                                       Timestamps
      │                                                            │
      │                                                            ▼
      └──▶ Extract Frame (OpenCV) ───────▶ Crop & OCR ─────────────┤
                                                                   │
                                                                   ▼
                                                            Save JSON Output
                                                        (Audio Text + Subtitle Text)
```

---

## 🛠️ Tech Stack

| Component        | Technology                                                          |
| ---------------- | ------------------------------------------------------------------- |
| Audio Extraction | [FFmpeg](https://ffmpeg.org/) via `ffmpeg-python`                   |
| Transcription    | [OpenAI Whisper](https://github.com/openai/whisper) (`base` model) |
| Similarity       | [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)               |
| Language         | Python 3.10+                                                       |

---

##  How to Run

### Prerequisites

1. **Python 3.10+** installed
2. **FFmpeg** installed and available in `PATH`

   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu / Debian
   sudo apt install ffmpeg

   # Windows (via Chocolatey)
   choco install ffmpeg
   ```

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/pr-mismatch-prototype.git
cd pr-mismatch-prototype

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# Using the default sample.mp4
python pipeline.py

# Or specify a custom video
python pipeline.py path/to/your/video.mp4
```

### Run Individual Modules

```bash
# Extract audio only
python extract_audio.py

# Transcribe only (requires audio.wav to exist)
python transcribe.py
```

---

##  Output Example

Running `python pipeline.py` generates an `output.json` file:

```json
[
  {
    "start": 0.0,
    "end": 2.14,
    "text": "Hello everyone"
  },
  {
    "start": 2.14,
    "end": 5.48,
    "text": "welcome to today's session on subtitling"
  },
  {
    "start": 5.48,
    "end": 8.92,
    "text": "we will discuss how to improve accessibility"
  }
]
```

The similarity demo also prints:

```text
[SIMILARITY] MISMATCH ✗
  Audio text:    "Hello everyone welcome to the session"
  Subtitle text: "Hello everyone, welcome to the sesion"
  Score:         91.8%  (threshold: 80.0%)
```

---

##  Project Structure

```text
pr-mismatch-prototype/
│
├── frame_extractor.py  # OpenCV frame extraction
├── ocr.py              # Subtitle cropping & OCR
├── extract_audio.py    # FFmpeg audio extraction
├── transcribe.py       # Whisper transcription
├── pipeline.py         # Main orchestrator + similarity demo
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── youtube_sample.mp4  # Your input video (not included)
└── output.json         # Generated output
```

---

##  Phase 2: OCR Integration

This phase extends the pipeline by capturing subtitles hardcoded into the video frames:

1. **Frame Extraction**: Extracts a video frame precisely at the midpoint of each Whisper transcription segment.
2. **Subtitle Region Cropping**: Crops the bottom 25% of the frame, assuming this is where subtitles are located.
3. **OCR**: Uses Tesseract OCR to read text from the cropped area, converting image to text.

### Limitations

* **OCR Accuracy**: Depends heavily on subtitle clarity, background contrast, and font.
* **No Mismatch Scoring**: This phase extracts both audio text and subtitle text but doesn't implement advanced mismatch scoring yet.
* **Language Support**: Currently only English (`eng`) is tested. Extending to Hindi/Kannada will require adding additional Tesseract language packs.

---

##  Future Work

This prototype is currently at **Phase 2**. Planned enhancements include:

| Phase   | Feature                              | Description                                                       |
| ------- | ------------------------------------ | ----------------------------------------------------------------- |
| Phase 3 | **Mismatch Detection**               | Align and compare transcribed audio against extracted subtitles    |
| Phase 4 | **HTML Report Generation**           | Generate visual reports highlighting mismatched segments           |
| Phase 5 | **Batch Processing & Dashboard**     | Process multiple videos and provide a web-based review interface   |

---

## My Contribution (Phase 1)

- Implemented audio extraction pipeline using FFmpeg
- Integrated Whisper for timestamp-based transcription
- Generated structured JSON output for downstream processing
- Designed modular pipeline for future OCR + mismatch detection

This serves as a foundational step toward full mismatch detection system.

---

<p align="center">
  Built with ❤️ for <strong>Planet Read</strong> under the <strong>C4GT</strong> program
</p>
