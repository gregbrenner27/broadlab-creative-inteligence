# Broadlab Creative Intelligence — Scoring Rubric

This rubric is the step-by-step guide Claude follows when producing resonance scores. Every score must be justified with specific evidence from the Creative Genome data.

---

## Scoring Principles

1. **Evidence-first:** Every score must cite specific data from the genome (e.g., "audio tempo of 142 BPM", "celebrity athlete detected", "transcript opens with a question").
2. **No inflation:** An average ad scores 5–6. Reserve 8–10 for genuinely exceptional creative.
3. **No rounding to round numbers:** Scores should reflect precise assessment (e.g., 6.5 is fine; everything being exactly 7 is suspicious).
4. **Persona-specific:** A score is meaningless without knowing who it is for. Always state the persona before scoring.

---

## Dimension 1: Emotional Power — Scoring Guide

Ask: *Does this ad generate a strong, sustained emotional response?*

Look for in the genome:
- Audio energy level (RMS) — high energy correlates with stronger emotional response
- Narrative arc — does it build to an emotional peak?
- Transcript — are there emotionally charged words or phrases?
- Rekognition — are there human faces expressing emotion? What emotions are detected?
- DAIVID cohort — what is the dominant cohort and how intense is it?

**Score 8–10:** Multiple emotional triggers converging; strong peak moment; positive or cathartic resolution; sustained throughout.
**Score 6–7:** Clear emotional intention; lands in key moments; may lose intensity in middle sections.
**Score 4–5:** Emotional intent is present but execution is inconsistent; some moments work, others are flat.
**Score 2–3:** Isolated emotional moments only; mostly informational or visually passive.
**Score 0–1:** No discernible emotional content.

---

## Dimension 2: Emotional Register Match — Scoring Guide

Ask: *Does the dominant DAIVID cohort match what this specific persona responds to?*

Cross-reference:
- The Creative Genome's DAIVID cohort classification
- The demographic response patterns in RESEARCH_FRAMEWORK.md
- The persona's stated primary motivation

**Exact cohort match:** Start at 8, adjust up/down based on intensity of cohort signal.
**Adjacent cohort match:** Start at 6.
**Unrelated cohort:** Start at 4.
**Actively mismatched cohort (e.g., Negative Adrenaline for older trust-seeking audience):** Start at 2.

---

## Dimension 3: Identity Signal Fit — Scoring Guide

Ask: *Would this persona feel this ad was made for them?*

Look for in the genome:
- Casting — age, gender, ethnicity, body type of people in the ad
- Setting — aspirational vs relatable vs neutral
- Language register — aspirational, functional, inclusive, exclusive?
- Cultural references — sport, music, lifestyle signals
- Product framing — how is the product positioned?

**Score 8–10:** Multiple strong identity signals pointing directly at this persona. No signals that exclude them.
**Score 6–7:** Clear but not exclusive targeting. Persona would feel included even if not uniquely targeted.
**Score 4–5:** Mixed signals. Persona might feel the ad is for someone slightly different.
**Score 2–3:** Signals consistently point to a different demographic. This persona is not represented.
**Score 0–1:** Active exclusion signals present.

---

## Dimension 4: Motivational Alignment — Scoring Guide

Ask: *Does the ad's core promise match what this persona fundamentally wants?*

Identify the ad's motivational promise from the genome:
- Transcript — what does the ad say the product will do for you?
- Visual narrative — what transformation or outcome is shown?
- CTA — what is the viewer asked to do and why?

Then match against the persona's primary motivation (Achievement, Belonging, Security, Status, Value).

**Score 8–10:** The ad's core promise is the persona's primary motivation stated clearly and compellingly.
**Score 6–7:** The ad's promise aligns with the persona's motivation but is not the explicit focus.
**Score 4–5:** The motivational promise is present as a secondary message.
**Score 2–3:** The ad promises something this persona does not care about.
**Score 0–1:** The ad's promise actively contradicts what this persona values.

---

## Dimension 5: Attention Architecture Fit — Scoring Guide

Ask: *Does the ad's structure match how this persona's attention works?*

Look for in the genome:
- Opening hook — what happens in the first 3 seconds?
- Pacing — cuts per minute (estimated from Rekognition label frequency)
- Narrative complexity — linear story vs fragmented vs montage
- Duration — total length of the ad
- Information density — how much new information per second?

Apply persona-specific attention profiles:
- **18–34:** Needs hook by second 3. High cutting is fine. Can handle fragmented structure.
- **35–44:** Moderate pace. Hook by second 5. Needs clear narrative thread.
- **45+:** Clear narrative structure required. Hook can be slower build. Fast cutting reduces comprehension.

**Score 8–10:** Structure is perfectly calibrated for this persona's attention profile.
**Score 6–7:** Good structural fit with minor misalignment.
**Score 4–5:** Structural issues present but persona can still follow the message.
**Score 2–3:** Structural mismatch is likely to cause attention drop-off before message lands.
**Score 0–1:** Ad structure is fundamentally incompatible with how this persona processes content.

---

## Strengths and Gaps Format

After scoring, identify exactly:

**Three Strengths:** The three dimensions or specific creative choices that most help this ad resonate with this persona. Be specific — cite the data.

**Two Gaps:** The two biggest creative weaknesses for this persona. State them as actionable observations, not just low scores.

---

## Budget Concentration Decision

Based on the Overall Resonance Score:

| Score | Decision | Language to use in report |
|-------|----------|--------------------------|
| 8.0–10.0 | High concentration | "Concentrate primary budget here. This persona is the natural audience for this creative." |
| 6.0–7.9 | Medium concentration | "Include with secondary budget weight. Creative resonates sufficiently but is not optimally tuned." |
| 4.0–5.9 | Low concentration / test | "Test at low spend only. Monitor performance closely before scaling." |
| 0–3.9 | Deprioritise | "Do not concentrate spend here. Creative is likely to underperform with this audience." |

---

## Red Flags — Auto-Escalate These

The following findings must be called out explicitly in the Creative Flags section regardless of overall score:

1. **Emotional Power below 5** — this is the most important possible flag
2. **Significant Confusion cohort score** — the ad is losing audiences somewhere
3. **Negative Adrenaline without resolution** — urgency that has no payoff
4. **No discernible hook in first 3 seconds** — critical for any audience under 45
5. **CTA absent or unclear** — the ad has no actionable endpoint
6. **Transcript-visual disconnect** — what is said and what is shown do not match
