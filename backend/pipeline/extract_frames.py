"""
extract_frames.py
-----------------
Pipeline Step 4: Extract key frames from the video as JPEG images.

Rather than analysing every single video frame (which would be thousands),
we take a snapshot once every 6 seconds. This gives us a representative
sample of what the ad looks like at each moment.

These frames are used by Claude (if configured with vision) to describe
what it sees. They're also useful for manual review.

Input:  path to the MP4 file
Output: list of JPEG file paths saved in a frames sub-folder of temp_dir
"""

import subprocess
import os
import json
import logging

logger = logging.getLogger(__name__)


def extract_frames(mp4_path: str, temp_dir: str, interval_seconds: int = 6) -> list:
    """
    Extract frames from an MP4 video at regular intervals.

    Parameters:
        mp4_path         - full file path to the input MP4 video
        temp_dir         - folder where frames sub-folder will be created
        interval_seconds - how many seconds between each extracted frame (default: 6)

    Returns:
        List of file paths to the extracted JPEG images
    """

    # Create a dedicated sub-folder for the frames
    frames_dir = os.path.join(temp_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    logger.info(f"Extracting frames every {interval_seconds}s from: {mp4_path}")

    # FFmpeg command to extract frames:
    # -i                = input file
    # -vf fps=1/N       = video filter: take 1 frame per N seconds
    # -q:v 2            = image quality (2 = high quality JPEG)
    # frame_%03d.jpg    = output filename pattern (frame_001.jpg, frame_002.jpg, etc.)
    ffmpeg_command = [
        "ffmpeg",
        "-i", mp4_path,
        "-vf", f"fps=1/{interval_seconds}",
        "-q:v", "2",
        "-y",
        os.path.join(frames_dir, "frame_%03d.jpg")
    ]

    try:
        subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg frame extraction failed: {e.stderr}")
        raise RuntimeError(f"Failed to extract frames: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("FFmpeg is not installed. Run: brew install ffmpeg")

    # Collect the paths of all extracted frames, sorted by time order
    frame_files = sorted([
        os.path.join(frames_dir, f)
        for f in os.listdir(frames_dir)
        if f.endswith(".jpg")
    ])

    logger.info(f"Extracted {len(frame_files)} frames")

    # Build frame metadata — each frame gets a timestamp based on its position
    frame_metadata = []
    for i, frame_path in enumerate(frame_files):
        timestamp_seconds = i * interval_seconds
        frame_metadata.append({
            "frame_index": i + 1,
            "timestamp_seconds": timestamp_seconds,
            "file_path": frame_path,
            "filename": os.path.basename(frame_path)
        })

    # Save frame metadata to JSON
    metadata_path = os.path.join(temp_dir, "frame_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump({
            "total_frames": len(frame_files),
            "interval_seconds": interval_seconds,
            "frames": frame_metadata
        }, f, indent=2)

    return frame_files
