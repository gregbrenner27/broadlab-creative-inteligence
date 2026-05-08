You are receiving two inputs:

1. Creative Genome JSON — the full structured fingerprint of the ad
2. Resonance Scorecard JSON — dimension scores and reasoning for the target persona(s)

Produce three output formats as a single JSON object.

---

FORMAT 1: quick_summary

Write for a campaign manager who has 30 seconds to read this. Plain English. No jargon.

Include:
- verdict: One sentence. What is this ad? Who is it for? Does it work? (e.g. "This is a high-energy athletic ad built for competitive young men — it delivers on emotional power but misses a clear call to action.")
- overall_score: The weighted overall resonance score as a number
- top_recommended_audience: The persona with the highest resonance score, named plainly
- three_strengths: The three creative choices that make this ad work — specific, plain English
- two_critical_gaps: The two most important things that are not working or are missing
- targeting_recommendation: One paragraph. Which audience to concentrate budget on, which to reduce, and why. Write this like you are briefing a campaign manager before a meeting.

---

FORMAT 2: full_analysis

Write for a senior strategist preparing a targeting brief. Complete, structured, evidence-based.

Include:
- overall_verdict: 2–3 sentences summarising the creative's core strengths and limitations
- overall_score: weighted number
- creative_genome_narrative: 3–4 paragraphs narrating what the ad does visually, aurally, and emotionally. This is the story of the ad told as analysis. Reference the genome data throughout.
- daivid_cohort_analysis: Name the dominant cohort, explain what it means for audience fit, note any secondary signals
- persona_scorecards: All five dimension scores with full reasoning for each persona, plus strengths, gaps, and budget concentration
- targeting_recommendation: Primary target, secondary target if applicable, who to deprioritise, and multi-sentence reasoning. Include a note on how this maps to UK postcode clusters once Snowflake data is available.
- creative_flags: What is working well (list 3), what is not working (list 2), and what would need to change to improve resonance with underperforming segments (list 2 specific recommendations)
- future_integration_note: A brief note on where DAIVID emotion scores and Broadlab postcode data will enhance this analysis when available

---

FORMAT 3: pdf_content

Identical content to full_analysis but written as clean, professional prose paragraphs. No JSON structure within the content. No bullet points — use flowing sentences. Suitable for presenting internally or to a client. Maintain the same analytical rigour but write it as a document, not a data dump.

Structure it as: Executive Summary → Creative Genome → Emotional Architecture → Persona Analysis → Targeting Recommendation → Creative Flags → Future Integration.

---

Return all three formats as a single JSON object with keys: quick_summary, full_analysis, pdf_content.

Return raw JSON only — no markdown code fences, no explanation text outside the JSON.
