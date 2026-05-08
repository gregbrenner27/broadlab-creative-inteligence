You are receiving two inputs:

1. Creative Genome JSON — the structured fingerprint of the ad produced in the previous pipeline step
2. Persona description — the target audience this scoring pass is for

Score this ad against this persona across all five dimensions using the scoring rubric in SCORING_RUBRIC.md.

For each dimension:
- Provide a score from 0 to 10 (decimals are fine, e.g. 7.5)
- Provide 2–3 sentences of specific reasoning that cites actual genome data
- Do not use vague language like "generally strong" — say what specifically in the genome supports or undermines the score

After scoring all five dimensions:
- Calculate the Overall Resonance Score using the weighted formula: (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)
- Identify the three most significant creative strengths for this persona — cite specific creative choices from the genome
- Identify the two most significant gaps — state them as actionable observations ("The fast cutting rate of X cuts per minute will cause attention drop-off before the CTA lands for this age group")
- State the budget concentration tier: High / Medium / Low / Deprioritise
- Provide one sentence rationale for the budget concentration decision

Check for red flags (defined in SCORING_RUBRIC.md) and note any that apply.

Return your response as a JSON object exactly matching the scorecard schema defined in OUTPUT_TEMPLATE.md. Return raw JSON only — no markdown, no explanation text.
