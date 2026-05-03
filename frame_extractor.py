"""
frame_extractor.py
------------------
Extracts specific frames from a video based on timestamps.
Part of the Planet Read - Audio-Subtitle Mismatch Detection prototype (Phase 2).
"""

import cv2
import os

def extract_frame(video_path: str, timestamp: float, output_path: str) -> str:
    """
    Extracts a single frame from the video at the given timestamp.

    Args:
        video_path: Path to the input video file.
        timestamp: Time in seconds where the frame should be extracted.
        output_path: Path to save the extracted frame image.

    Returns:
        Path to the saved image, or None if extraction failed.
    """
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        return None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open video: {video_path}")
        return None

    # Get FPS and calculate frame index
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("[ERROR] Could not determine FPS.")
        cap.release()
        return None

    frame_index = int(timestamp * fps)
    
    # Set video position to the calculated frame index
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"[ERROR] Could not read frame at {timestamp}s (index {frame_index}).")
        return None

    # Save the frame
    cv2.imwrite(output_path, frame)
    return output_path

if __name__ == "__main__":
    # Simple test
    extract_frame("sample.mp4", 2.0, "test_frame.jpg")
