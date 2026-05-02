"""
transcribe.py
-------------
Transcribes audio using OpenAI Whisper and returns timestamped segments.
Part of the Planet Read - Audio-Subtitle Mismatch Detection prototype.
"""

import os
import whisper


def transcribe_audio(
    audio_path: str = "audio.wav",
    model_name: str = "base",
) -> list[dict]:
    """
    Transcribe an audio file and return timestamped text segments.

    Args:
        audio_path:  Path to the input audio file (.wav).
        model_name:  Whisper model size (tiny, base, small, medium, large).

    Returns:
        A list of segment dicts with keys: start, end, text.

    Raises:
        FileNotFoundError: If the audio file does not exist.
    """
    # --- Validate input ---
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"[ERROR] Audio file not found: {audio_path}")

    print(f"[INFO] Loading Whisper model: {model_name}")
    model = whisper.load_model(model_name)

    print(f"[INFO] Transcribing: {audio_path}")
    result = model.transcribe(audio_path)

    # --- Build structured output ---
    segments = []
    for seg in result.get("segments", []):
        segment = {
            "start": round(seg["start"], 2),
            "end":   round(seg["end"], 2),
            "text":  seg["text"].strip(),
        }
        segments.append(segment)
        print(f"  [{segment['start']:.2f} → {segment['end']:.2f}] {segment['text']}")

    print(f"[OK] Transcription complete — {len(segments)} segment(s) found.")
    return segments


# ---------------------------------------------------------------------------
# Quick standalone test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    transcribe_audio()
