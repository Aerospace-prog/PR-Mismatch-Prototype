"""
pipeline.py
-----------
Main orchestrator for the Audio-Subtitle Mismatch Detection prototype.

Usage:
    python pipeline.py                    # defaults to sample.mp4
    python pipeline.py path/to/video.mp4  # custom video

Part of the Planet Read - C4GT project.
"""

import json
import os
import sys

from extract_audio import extract_audio
from transcribe import transcribe_audio


# ---------------------------------------------------------------------------
# Optional: Similarity demo (rapidfuzz)
# ---------------------------------------------------------------------------

def similarity_check(
    text_a: str,
    text_b: str,
    threshold: float = 80.0,
) -> dict:
    """
    Compare two strings and flag a mismatch if similarity is below threshold.

    Args:
        text_a:    First string  (e.g. transcribed audio).
        text_b:    Second string (e.g. subtitle text).
        threshold: Minimum similarity score (0–100) to consider a match.

    Returns:
        A dict with keys: text_a, text_b, similarity, is_match.
    """
    try:
        from rapidfuzz import fuzz
    except ImportError:
        print("[WARN] rapidfuzz is not installed — skipping similarity check.")
        return {}

    score = fuzz.ratio(text_a, text_b)
    is_match = score >= threshold

    status = "MATCH ✓" if is_match else "MISMATCH ✗"
    print(f"\n[SIMILARITY] {status}")
    print(f"  Audio text:    \"{text_a}\"")
    print(f"  Subtitle text: \"{text_b}\"")
    print(f"  Score:         {score:.1f}%  (threshold: {threshold}%)")

    return {
        "text_a":     text_a,
        "text_b":     text_b,
        "similarity": round(score, 2),
        "is_match":   is_match,
    }


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    video_path: str = "sample.mp4",
    output_path: str = "output.json",
    model_name: str = "base",
) -> None:
    """
    End-to-end pipeline: extract audio → transcribe → save JSON.

    Args:
        video_path:  Path to the input video.
        output_path: Path for the output JSON file.
        model_name:  Whisper model to use.
    """
    print("=" * 60)
    print("  Planet Read — Audio-Subtitle Mismatch Detection")
    print("  Phase 1: Transcription Pipeline")
    print("=" * 60)

    # Step 1 — Extract audio
    print("\n▶ STEP 1: Audio Extraction")
    audio_path = extract_audio(video_path)

    # Step 2 — Transcribe
    print("\n▶ STEP 2: Whisper Transcription")
    segments = transcribe_audio(audio_path, model_name=model_name)

    # Step 3 — Save JSON output
    print("\n▶ STEP 3: Saving Output")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)
    print(f"[OK] Results saved to: {output_path}")

    # Step 4 — Optional similarity demo
    print("\n▶ STEP 4: Similarity Demo")
    similarity_check(
        text_a="Hello everyone welcome to the session",
        text_b="Hello everyone, welcome to the sesion",  # intentional typo
    )

    # Summary
    print("\n" + "=" * 60)
    print(f"   Pipeline complete.")
    print(f"   Segments: {len(segments)}")
    print(f"   Output:   {os.path.abspath(output_path)}")
    print("=" * 60)


# Entry point
if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "sample.mp4"
    run_pipeline(video_path=video)
