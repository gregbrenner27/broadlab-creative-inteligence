"""
resonance_call.py
-----------------
Pipeline Step 7: Score the ad against the target persona using Claude AI.

This is the second Claude call. It takes the Creative Genome from Step 6
and the user's target audience description, and asks Claude to score the
ad across all five dimensions (Emotional Power, Register Match, Identity
Fit, Motivational Alignment, Attention Architecture).

The output is a structured scorecard with numerical scores, reasoning,
strengths, gaps, and a budget concentration recommendation.

Input:  genome.json + persona description from user
Output: scorecard.json — the Resonance Scorecard
"""

import anthropic
import json
import os
import logging

logger = logging.getLogger(__name__)

PROMPTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "prompts"
)

FRAMEWORK_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "framework"
)


def _load_prompt(filename: str) -> str:
    """Load a file from the prompts directory."""
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r") as f:
        return f.read().strip()


def _load_framework(filename: str) -> str:
    """Load a file from the framework directory."""
    path = os.path.join(FRAMEWORK_DIR, filename)
    with open(path, "r") as f:
        return f.read().strip()


def score_resonance(
    genome: dict,
    brand_context: dict,
    anthropic_api_key: str,
    temp_dir: str
) -> dict:
    """
    Call Claude to score the ad's resonance against the target persona.

    Parameters:
        genome            - the Creative Genome dict from genome_call.py
        brand_context     - user input including target_audience and primary_motivation
        anthropic_api_key - from .env: ANTHROPIC_API_KEY
        temp_dir          - folder where scorecard.json will be saved

    Returns:
        Dictionary containing the Resonance Scorecard
    """

    logger.info("Scoring resonance with Claude...")

    # Load prompts and framework documents
    system_prompt = _load_prompt("SYSTEM_PROMPT.md")
    resonance_prompt = _load_prompt("RESONANCE_PROMPT.md")
    scoring_rubric = _load_framework("SCORING_RUBRIC.md")

    # Build the persona object from user inputs
    # The system maps the user's plain-English description to a structured persona
    persona = {
        "name": _derive_persona_name(brand_context),
        "description": brand_context.get("target_audience", "Not specified"),
        "primary_motivation": brand_context.get("primary_motivation", "Achievement"),
        "secondary_audience": brand_context.get("secondary_audience", None)
    }

    user_message = f"""{resonance_prompt}

---

## SCORING RUBRIC (reference this throughout)

{scoring_rubric}

---

## INPUT 1: Creative Genome

```json
{json.dumps(genome, indent=2)}
```

---

## INPUT 2: Target Persona

```json
{json.dumps(persona, indent=2)}
```

---

Score this ad against this persona now. Apply the weighted formula: Overall = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10). Return raw JSON only."""

    client = anthropic.Anthropic(api_key=anthropic_api_key)

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    response_text = response.content[0].text.strip()
    logger.info(f"Claude resonance response received ({len(response_text)} chars)")

    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start != -1 and end > start:
        response_text = response_text[start:end]

    try:
        scorecard = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude resonance response as JSON: {e}")
        logger.error(f"Raw response (last 300 chars): {response_text[-300:]}")
        raise RuntimeError(f"Claude returned invalid JSON for scorecard: {e}")

    # Save to file
    output_path = os.path.join(temp_dir, "scorecard.json")
    with open(output_path, "w") as f:
        json.dump(scorecard, f, indent=2)

    logger.info("Resonance scoring complete")
    return scorecard


def _derive_persona_name(brand_context: dict) -> str:
    """
    Create a short persona name from the motivation and audience description.
    Used as a label in the output report.
    """
    motivation = brand_context.get("primary_motivation", "Achievement")
    audience = brand_context.get("target_audience", "")

    # Extract a short label from the first few words of the audience description
    words = audience.split()[:4]
    short_desc = " ".join(words) if words else "Target Audience"

    return f"{short_desc} ({motivation}-motivated)"
