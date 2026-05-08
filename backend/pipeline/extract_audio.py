"""
extract_audio.py
----------------
Pipeline Step 1: Extract the audio track from the uploaded MP4 video.

Uses FFmpeg (a command-line video tool) to pull out just the sound from
the video and save it as a WAV file. WAV is an uncompressed audio format
that Librosa (Step 2) and Whisper (Step 3) can read reliably.

Input:  path to the uploaded MP4 file
Output: path to the extracted WAV file saved in the temp folder
"""

import subprocess  # allows Python to run command-line programs like FFmpeg
import os
import logging

logger = logging.getLogger(__name__)


def extract_audio(mp4_path: str, temp_dir: str) -> str:
    """
    Extract audio from an MP4 file and save as WAV.

    Parameters:
        mp4_path  - full file path to the input MP4 video
        temp_dir  - folder where the WAV file will be saved

    Returns:
        Full file path to the output WAV file

    Raises:
        RuntimeError if FFmpeg is not installed or the extraction fails
    """

    # Build the output file path — same name as the video but with .wav extension
    video_filename = os.path.splitext(os.path.basename(mp4_path))[0]
    wav_path = os.path.join(temp_dir, f"{video_filename}_audio.wav")

    logger.info(f"Extracting audio from: {mp4_path}")
    logger.info(f"Output WAV path: {wav_path}")

    # FFmpeg command to extract audio:
    # -i          = input file
    # -vn         = no video (audio only)
    # -acodec pcm = use PCM encoding (uncompressed WAV)
    # -ar 44100   = set sample rate to 44100 Hz (CD quality, what Whisper expects)
    # -ac 1       = mono channel (Librosa and Whisper both work with mono)
    # -y          = overwrite output file if it already exists
    ffmpeg_command = [
        "ffmpeg",
        "-i", mp4_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "1",
        "-y",
        wav_path
    ]

    try:
        # Run the FFmpeg command and capture any error output
        result = subprocess.run(
            ffmpeg_command,
            capture_output=True,  # capture stdout and stderr so we can log them
            text=True,            # decode output as text (not raw bytes)
            check=True            # raise an exception if FFmpeg returns an error code
        )
        logger.info("Audio extraction completed successfully")
        return wav_path

    except subprocess.CalledProcessError as e:
        # FFmpeg returned a non-zero exit code — something went wrong
        logger.error(f"FFmpeg audio extraction failed: {e.stderr}")
        raise RuntimeError(
            f"Failed to extract audio from video. "
            f"Make sure FFmpeg is installed (run: brew install ffmpeg). "
            f"FFmpeg error: {e.stderr}"
        )
    except FileNotFoundError:
        # FFmpeg is not installed on this machine
        raise RuntimeError(
            "FFmpeg is not installed. Install it by running: brew install ffmpeg"
        )
