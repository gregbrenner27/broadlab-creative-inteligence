"""
synthesis_call.py
-----------------
Pipeline Step 8: Generate the final report using Claude AI.

This is the third and final Claude call. It takes the Creative Genome and
the Resonance Scorecard and asks Claude to produce three versions of the
final report:
  1. Quick Summary — for a 30-second scan
  2. Full Analysis — complete scoring breakdown and targeting recommendation
  3. PDF Content — same content in clean prose format for export

The output feeds directly into the frontend display and the PDF generator.

Input:  genome.json + scorecard.json
Output: report.json — the complete final report in all three formats
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


def _load_prompt(filename: str) -> str:
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r") as f:
        return f.read().strip()


def generate_final_report(
    genome: dict,
    scorecard: dict,
    brand_context: dict,
    anthropic_api_key: str,
    temp_dir: str
) -> dict:
    """
    Call Claude to generate the final report in three formats.

    Parameters:
        genome            - the Creative Genome dict from genome_call.py
        scorecard         - the Resonance Scorecard dict from resonance_call.py
        brand_context     - user input for context
        anthropic_api_key - from .env: ANTHROPIC_API_KEY
        temp_dir          - folder where report.json will be saved

    Returns:
        Dictionary with keys: quick_summary, full_analysis, pdf_content
    """

    logger.info("Generating final report with Claude...")

    system_prompt = _load_prompt("SYSTEM_PROMPT.md")
    synthesis_prompt = _load_prompt("SYNTHESIS_PROMPT.md")

    user_message = f"""{synthesis_prompt}

---

## Campaign Context

Brand: {brand_context.get('brand_name', 'Unknown')}
Category: {brand_context.get('category', 'Unknown')}
Campaign Goal: {brand_context.get('campaign_goal', 'Not specified')}

---

## INPUT 1: Creative Genome

```json
{json.dumps(genome, indent=2)}
```

---

## INPUT 2: Resonance Scorecard

```json
{json.dumps(scorecard, indent=2)}
```

---

Produce all three formats now (quick_summary, full_analysis, pdf_content) as a single JSON object. Return raw JSON only."""

    client = anthropic.Anthropic(api_key=anthropic_api_key)

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,  # final report is longer so we allow more tokens
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    response_text = response.content[0].text.strip()
    logger.info(f"Claude synthesis response received ({len(response_text)} chars)")

    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start != -1 and end > start:
        response_text = response_text[start:end]

    try:
        report = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude synthesis response as JSON: {e}")
        logger.error(f"Raw response (last 300 chars): {response_text[-300:]}")
        raise RuntimeError(f"Claude returned invalid JSON for final report: {e}")

    # Wrap in the 'report' key to match the output schema
    full_report = {"report": report} if "report" not in report else report

    # Save to file
    output_path = os.path.join(temp_dir, "report.json")
    with open(output_path, "w") as f:
        json.dump(full_report, f, indent=2)

    logger.info("Final report generated successfully")
    return full_report
