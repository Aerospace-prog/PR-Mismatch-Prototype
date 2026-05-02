"""
extract_audio.py
----------------
Extracts audio from a video file using FFmpeg.
Part of the Planet Read - Audio-Subtitle Mismatch Detection prototype.
"""

import os
import ffmpeg


def extract_audio(video_path: str, audio_path: str = "audio.wav") -> str:
    """
    Extract audio track from a video file and save as WAV.

    Args:
        video_path: Path to the input video file (.mp4).
        audio_path: Path for the output audio file (.wav).

    Returns:
        Path to the extracted audio file.

    Raises:
        FileNotFoundError: If the input video file does not exist.
        RuntimeError: If FFmpeg fails during extraction.
    """
    # --- Validate input ---
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"[ERROR] Video file not found: {video_path}")

    print(f"[INFO] Extracting audio from: {video_path}")

    try:
        # Build and run the FFmpeg pipeline
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, ac=1, ar=16000)  # mono, 16 kHz — optimal for Whisper
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(
            f"[ERROR] FFmpeg failed during audio extraction.\n"
            f"Stderr: {e.stderr.decode() if e.stderr else 'N/A'}"
        ) from e

    print(f"[OK] Audio saved to: {audio_path}")
    return audio_path


# ---------------------------------------------------------------------------
# Quick standalone test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    extract_audio("sample.mp4")
