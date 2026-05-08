"""
genome_call.py
--------------
Pipeline Step 6: Generate the Creative Genome using Claude AI.

This is the first of three Claude calls. It takes all five data inputs
from the pipeline (audio features, transcript, Rekognition visuals, frame
metadata, and user-provided brand context) and asks Claude to synthesise
them into a structured "Creative Genome" — a fingerprint of what this ad
is doing emotionally, visually, and narratively.

The output is a structured JSON that feeds into Steps 7 and 8.

Input:  all pipeline outputs + brand/campaign context from user
Output: genome.json — the Creative Genome
"""

import anthropic
import json
import os
import logging

logger = logging.getLogger(__name__)

# Path to the prompts directory — relative to this file's location
PROMPTS_DIR = os.path.join(
    os.path.dirname(__file__),  # backend/claude/
    "..",                        # backend/
    "..",                        # broadlab-creative-intelligence/
    "prompts"
)


def _load_prompt(filename: str) -> str:
    """Load a prompt file from the prompts directory."""
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r") as f:
        return f.read().strip()


def generate_creative_genome(
    audio_features: dict,
    transcript: dict,
    rekognition: dict,
    frame_metadata: dict,
    brand_context: dict,
    anthropic_api_key: str,
    temp_dir: str
) -> dict:
    """
    Call Claude to generate the Creative Genome from all pipeline inputs.

    Parameters:
        audio_features    - from analyse_audio.py
        transcript        - from transcribe.py
        rekognition       - from run_rekognition.py
        frame_metadata    - from extract_frames.py
        brand_context     - user input: brand name, category, goal, audience, motivation
        anthropic_api_key - from .env: ANTHROPIC_API_KEY
        temp_dir          - folder where genome.json will be saved

    Returns:
        Dictionary containing the Creative Genome
    """

    logger.info("Generating Creative Genome with Claude...")

    # Load the system and genome prompts from the prompts folder
    system_prompt = _load_prompt("SYSTEM_PROMPT.md")
    genome_prompt = _load_prompt("GENOME_PROMPT.md")

    # Build the user message — this is everything Claude will analyse
    # We structure it clearly so Claude can reference each input distinctly
    user_message = f"""{genome_prompt}

---

## INPUT 1: Brand and Campaign Context (provided by user)

Brand: {brand_context.get('brand_name', 'Unknown')}
Category: {brand_context.get('category', 'Unknown')}
Campaign Goal: {brand_context.get('campaign_goal', 'Not specified')}
Target Audience Description: {brand_context.get('target_audience', 'Not specified')}
Primary Motivation: {brand_context.get('primary_motivation', 'Not specified')}
Additional Context: {brand_context.get('additional_context', 'None provided')}

---

## INPUT 2: Audio Features (from Librosa analysis)

```json
{json.dumps(audio_features, indent=2)}
```

---

## INPUT 3: Speech Transcript (from OpenAI Whisper)

```json
{json.dumps(transcript, indent=2)}
```

---

## INPUT 4: Visual Analysis (from AWS Rekognition)

```json
{json.dumps(rekognition, indent=2)}
```

---

## INPUT 5: Frame Metadata (from FFmpeg frame extraction)

```json
{json.dumps(frame_metadata, indent=2)}
```

---

Now synthesise all five inputs into the Creative Genome JSON as specified in the GENOME_PROMPT above. Return raw JSON only."""

    # Call Claude API
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # Extract the response text
    response_text = response.content[0].text.strip()
    logger.info(f"Claude genome response received ({len(response_text)} chars)")

    # Strip markdown code fences if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    # Find the outermost JSON object in the response — handles any stray text
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start != -1 and end > start:
        response_text = response_text[start:end]

    try:
        genome = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude genome response as JSON: {e}")
        logger.error(f"Raw response (last 300 chars): {response_text[-300:]}")
        raise RuntimeError(f"Claude returned invalid JSON for genome: {e}")

    # Save to file
    output_path = os.path.join(temp_dir, "genome.json")
    with open(output_path, "w") as f:
        json.dump(genome, f, indent=2)

    logger.info("Creative Genome generated successfully")
    return genome
