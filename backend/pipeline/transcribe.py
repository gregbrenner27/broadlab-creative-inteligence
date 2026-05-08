"""
transcribe.py
-------------
Pipeline Step 3: Transcribe speech in the audio using OpenAI Whisper.

Whisper is an AI model from OpenAI that converts spoken audio into text.
We send it the WAV file extracted in Step 1 and receive back a full
transcript with word-level timestamps — useful for finding exactly when
key phrases appear in the ad.

If there is no speech in the ad (music-only), Whisper will return an
empty transcript, which Claude handles gracefully.

Input:  path to the WAV file from Step 1
Output: transcript dictionary saved as transcript.json
"""

import openai
import json
import os
import logging

logger = logging.getLogger(__name__)


def transcribe_audio(wav_path: str, temp_dir: str, openai_api_key: str) -> dict:
    """
    Transcribe speech from a WAV file using OpenAI Whisper.

    Parameters:
        wav_path       - full file path to the input WAV file
        temp_dir       - folder where transcript.json will be saved
        openai_api_key - your OpenAI API key from the .env file

    Returns:
        Dictionary containing transcript text, segments, and word timestamps
    """

    logger.info(f"Transcribing audio: {wav_path}")

    # Initialise the OpenAI client with your API key
    client = openai.OpenAI(api_key=openai_api_key)

    # Open the WAV file and send it to Whisper
    # response_format="verbose_json" gives us timestamps, not just plain text
    with open(wav_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",  # returns timestamps alongside text
            timestamp_granularities=["word", "segment"]  # word-level precision
        )

    # Extract the full transcript text
    full_text = response.text.strip()
    logger.info(f"Transcript length: {len(full_text)} characters")

    if not full_text:
        logger.info("No speech detected in audio (music-only or silent ad)")

    # Build the output dictionary
    # response.segments gives us sentence-level chunks with start/end times
    # response.words gives us individual word timestamps
    segments = []
    if hasattr(response, 'segments') and response.segments:
        for seg in response.segments:
            segments.append({
                "id": seg.id,
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": seg.text.strip()
            })

    words = []
    if hasattr(response, 'words') and response.words:
        for word in response.words:
            words.append({
                "word": word.word,
                "start": round(word.start, 2),
                "end": round(word.end, 2)
            })

    transcript_data = {
        "full_text": full_text,
        "has_speech": bool(full_text),
        "language": getattr(response, 'language', 'en'),
        "duration_seconds": getattr(response, 'duration', None),
        "segments": segments,
        "words": words,
        # Key phrases are the first and last 5 words — Claude uses these for hook/CTA detection
        "opening_words": full_text.split()[:5] if full_text else [],
        "closing_words": full_text.split()[-5:] if full_text else []
    }

    # Save to JSON file
    output_path = os.path.join(temp_dir, "transcript.json")
    with open(output_path, "w") as f:
        json.dump(transcript_data, f, indent=2)

    logger.info("Transcription complete")
    return transcript_data
