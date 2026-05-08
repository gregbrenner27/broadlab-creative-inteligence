"""
analyse_frames.py
-----------------
Pipeline Step 5 (replacement for AWS Rekognition): Analyse video frames using Claude Vision.

Instead of AWS Rekognition, we send the extracted JPEG frames directly to Claude AI,
which can see and describe what is happening in each frame. This means:
- No AWS account or credentials needed
- Works immediately with the existing Anthropic API key
- Any employee can use it — fully self-service
- Claude's descriptions are richer than raw Rekognition labels for creative analysis

We select up to 10 frames spread evenly across the video duration,
send them all in one Claude call, and receive back a structured visual analysis.

Input:  list of JPEG frame file paths from extract_frames.py
Output: visual_analysis.json — Claude's structured description of the visual content
"""

import anthropic
import base64
import json
import os
import logging

logger = logging.getLogger(__name__)

# Maximum number of frames to send to Claude — beyond this, costs increase
# and returns diminish. 10 frames covers a 60-second ad every 6 seconds.
MAX_FRAMES = 10


def analyse_frames_with_claude(
    frame_files: list,
    frame_metadata: dict,
    temp_dir: str,
    anthropic_api_key: str
) -> dict:
    """
    Send extracted video frames to Claude Vision for visual analysis.

    Parameters:
        frame_files       - list of JPEG file paths from extract_frames.py
        frame_metadata    - metadata dict including timestamps per frame
        temp_dir          - folder where visual_analysis.json will be saved
        anthropic_api_key - from .env: ANTHROPIC_API_KEY

    Returns:
        Dictionary containing structured visual analysis
    """

    if not frame_files:
        logger.warning("No frames provided for visual analysis")
        return _empty_analysis()

    # Select a representative sample of frames if there are more than MAX_FRAMES
    # We space them evenly so we cover the whole ad, not just the beginning
    selected_frames = _select_frames(frame_files, MAX_FRAMES)
    logger.info(f"Analysing {len(selected_frames)} frames with Claude Vision")

    # Build the message content — a mix of text instructions and images
    # Claude accepts images as base64-encoded strings alongside text
    content = []

    content.append({
        "type": "text",
        "text": """You are analysing frames from a video advertisement.

For each frame provided, note what you observe. Then produce a single structured JSON analysis of the overall visual profile of the ad.

Your analysis must include:

1. **settings**: Where does the ad take place? (e.g. indoor gym, outdoor stadium, city street, abstract/studio)
2. **dominant_subjects**: What are the main subjects? (e.g. athletes, families, products, abstract imagery)
3. **people_present**: Describe the people visible — approximate age range, apparent demographics, how they are dressed, what they are doing
4. **activities**: What actions or activities are shown?
5. **production_quality**: How is it shot? (e.g. cinematic/high-budget, raw/documentary, studio/clean, fast-cutting montage)
6. **colour_palette**: Describe the dominant colour treatment (e.g. high contrast, desaturated, warm tones, cool tones, black and white)
7. **pacing_impression**: Based on the frames, does the ad appear fast-cutting, moderate, or slow and deliberate?
8. **emotional_register**: What emotional tone do the visuals convey? (e.g. intense and competitive, warm and human, aspirational and sleek)
9. **identity_signals**: Who does this ad appear to be speaking to, based purely on visual cues?
10. **notable_elements**: Any standout visual choices — unusual framing, text on screen, product close-ups, symbolic imagery

Return ONLY a valid JSON object with these exact keys. No other text."""
    })

    # Add each frame as a base64 image
    frames_metadata_list = frame_metadata.get("frames", [])
    for i, frame_path in enumerate(selected_frames):
        # Get the timestamp for this frame from metadata
        timestamp = _get_timestamp(frame_path, frames_metadata_list)

        content.append({
            "type": "text",
            "text": f"Frame {i + 1} (at {timestamp}s):"
        })

        # Read the image file and encode it as base64
        # Base64 is a way of converting binary image data into text that can be sent in JSON
        with open(frame_path, "rb") as img_file:
            image_data = base64.standard_b64encode(img_file.read()).decode("utf-8")

        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_data
            }
        })

    # Call Claude Vision
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": content}
        ]
    )

    response_text = response.content[0].text.strip()
    logger.info(f"Claude Vision response received ({len(response_text)} chars)")

    # Strip markdown fences if Claude included them
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    try:
        visual_analysis = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude Vision response as JSON: {e}")
        logger.error(f"Raw response: {response_text[:300]}")
        # If JSON parsing fails, wrap the raw text in a basic structure
        visual_analysis = {
            "settings": "Analysis unavailable",
            "dominant_subjects": [],
            "people_present": response_text[:500],
            "activities": [],
            "production_quality": "Unknown",
            "colour_palette": "Unknown",
            "pacing_impression": "Unknown",
            "emotional_register": "Unknown",
            "identity_signals": "Unknown",
            "notable_elements": []
        }

    # Add metadata about how many frames were analysed
    visual_analysis["frames_analysed"] = len(selected_frames)
    visual_analysis["total_frames_available"] = len(frame_files)

    # Save to file
    output_path = os.path.join(temp_dir, "visual_analysis.json")
    with open(output_path, "w") as f:
        json.dump(visual_analysis, f, indent=2)

    logger.info("Frame analysis complete")
    return visual_analysis


def _select_frames(frame_files: list, max_count: int) -> list:
    """Select up to max_count frames evenly spaced across the full list."""
    if len(frame_files) <= max_count:
        return frame_files

    # Pick indices evenly spaced from start to end
    step = len(frame_files) / max_count
    indices = [int(i * step) for i in range(max_count)]
    return [frame_files[i] for i in indices]


def _get_timestamp(frame_path: str, frames_metadata: list) -> int:
    """Look up the timestamp for a frame by matching its filename."""
    filename = os.path.basename(frame_path)
    for frame in frames_metadata:
        if frame.get("filename") == filename:
            return frame.get("timestamp_seconds", 0)
    return 0


def _empty_analysis() -> dict:
    """Return a blank analysis when no frames are available."""
    return {
        "settings": "No frames available",
        "dominant_subjects": [],
        "people_present": "No frames available",
        "activities": [],
        "production_quality": "Unknown",
        "colour_palette": "Unknown",
        "pacing_impression": "Unknown",
        "emotional_register": "Unknown",
        "identity_signals": "Unknown",
        "notable_elements": [],
        "frames_analysed": 0,
        "total_frames_available": 0
    }
