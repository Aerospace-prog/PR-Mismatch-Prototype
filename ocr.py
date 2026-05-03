"""
ocr.py
------
Extracts subtitle text from a video frame using Tesseract OCR.
Assumes subtitles are located in the bottom 25% of the frame.
Part of the Planet Read - Audio-Subtitle Mismatch Detection prototype (Phase 2).
"""

import cv2
import pytesseract
import os

def extract_subtitle_text(image_path: str) -> str:
    """
    Reads an image, crops the bottom 25%, and extracts text using OCR.

    Args:
        image_path: Path to the input image frame.

    Returns:
        Extracted text as a string.
    """
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return ""

    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Could not read image: {image_path}")
        return ""

    # Crop the bottom 25% (subtitle region)
    height = img.shape[0]
    crop_top = int(height * 0.75)
    crop = img[crop_top:height, :]

    # Convert to grayscale for better OCR accuracy
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Apply OCR
    try:
        text = pytesseract.image_to_string(gray, lang="eng")
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return ""

if __name__ == "__main__":
    # Simple test
    print(extract_subtitle_text("test_frame.jpg"))
