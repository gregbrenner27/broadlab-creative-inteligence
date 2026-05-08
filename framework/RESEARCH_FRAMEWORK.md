# Broadlab Creative Intelligence — Research Framework

This document encodes the complete analytical methodology used by the Creative Intelligence Platform. Every Claude AI call references this framework when scoring ads.

---

## The Five Scoring Dimensions

Every ad is scored 0–10 across five dimensions for each audience persona.

### Dimension 1 — Emotional Power
**What it measures:** How strongly does the ad make people feel something?

Research from System1 across 125,000 ads confirms that emotional content is almost twice as effective as rational content. Ads generating strong emotional responses are up to four times more likely to drive long-term brand equity. An ad that generates no strong emotion will underperform regardless of targeting quality.

**Critical threshold:** If an ad scores below 5 here, that is the most important flag regardless of everything else. This is the baseline gate.

**Scoring guide:**
- 0–3: Flat, passive, no discernible emotional signal
- 4–5: Mild emotional moments, inconsistent delivery
- 6–7: Clear emotional intent, achieves resonance in key moments
- 8–9: Strong, sustained emotional engagement throughout
- 10: Exceptional — likely to generate strong recall and brand equity

---

### Dimension 2 — Emotional Register Match
**What it measures:** Does the dominant emotional cohort of the ad match what this specific audience responds to?

Based on the DAIVID 39-emotion framework organised into six cohorts (see below). Different audiences respond to fundamentally different emotional registers.

**Scoring guide:**
- 0–3: Significant mismatch — dominant cohort actively alienates this audience
- 4–5: Partial match — some alignment but dominant register is off
- 6–7: Good match — primary cohort resonates with this audience
- 8–10: Excellent match — emotional register is precisely calibrated for this audience

---

### Dimension 3 — Identity Signal Fit
**What it measures:** Do the visual signals — casting, setting, colour, pacing — make this audience feel the ad is speaking to them?

People decide within seconds whether an ad feels like it is for them. This is the "is this for me" signal. Identity signals include: who is in the ad, where the ad is set, cultural references, language register, product framing.

**Scoring guide:**
- 0–3: Audience is likely to feel excluded or that the ad is for someone else
- 4–5: Neutral — does not actively exclude but does not include either
- 6–7: Clear signals that this audience is in the intended target
- 8–10: The audience should feel this ad was made specifically for them

---

### Dimension 4 — Motivational Alignment
**What it measures:** Does the ad's core motivational promise match the primary motivational driver of this audience?

**Five motivational states:**
1. **Achievement and Mastery** — driven by performance, progress, winning
2. **Belonging and Social Validation** — driven by acceptance, community, connection
3. **Security and Reliability** — driven by trust, consistency, reduced risk
4. **Status and Aspiration** — driven by exclusivity, elevation, being admired
5. **Value and Fairness** — driven by getting a good deal, not being exploited

**Scoring guide:**
- 0–3: Ad promises something this audience does not care about
- 4–5: Motivational promise is present but secondary to the ad's main message
- 6–7: Clear alignment between ad promise and audience motivation
- 8–10: The ad's core message precisely targets this audience's primary driver

---

### Dimension 5 — Attention Architecture Fit
**What it measures:** Does the ad's pacing, structure, opening hook, and narrative complexity match what this audience's attention patterns can absorb?

Young audiences trained on short-form video need immediate hooks and fast information density. Older audiences need clarity and narrative structure. Getting this wrong means the audience tunes out before the message lands.

**Scoring guide:**
- 0–3: Structural mismatch — the ad will lose this audience before it makes its point
- 4–5: Partial fit — some elements work but key moments miss the attention window
- 6–7: Good structural fit — the ad holds attention for this audience
- 8–10: Perfectly calibrated — pacing and structure maximise engagement for this audience

---

## The DAIVID 39-Emotion Framework — Six Cohorts

### Cohort 1: Positive Adrenaline
**Emotions:** Excitement, Awe, Surprise, Triumph, Sexual Desire

**Maps to:** Young competitive sports audiences, gaming audiences, betting audiences. High scores here signal strong fit for achievement-motivated 18–34 demographics.

**Creative signals that activate this cohort:** Fast cutting, high-energy music, athletic or competitive imagery, surprising reveals, bold visual treatment, celebrity athletes.

---

### Cohort 2: Empathy
**Emotions:** Admiration, Calmness, Empathetic Pain, Gratitude, Hope, Pride, Relief, Sadness, Nostalgia, Love

**Maps to:** Older audiences 45+, family-oriented segments, trust-motivated buyers. High scores here signal strong fit for security and belonging motivated demographics.

**Creative signals that activate this cohort:** Real people, slower pacing, narrative storytelling, family and community settings, music with emotional warmth, moments of human connection.

---

### Cohort 3: Approach
**Emotions:** Adoration, Aesthetic Appreciation, Amusement, Entrancement, Craving, Inspiration, Interest, Joy, Knowledge, Satisfaction

**Maps to:** Aspiration-driven audiences, lifestyle segments, discovery-oriented buyers. Broadly appealing — works across demographics but especially with status and aspiration motivations.

**Creative signals that activate this cohort:** Beautiful product photography, satisfying demonstrations, aspirational lifestyle settings, clever or witty writing, moments of delight or discovery.

---

### Cohort 4: Negative Adrenaline
**Emotions:** Anger, Fear, Tension, Contempt, Disgust

**Usage note:** Used intentionally to create urgency or highlight problems. High scores without resolution into positive emotions is a **creative red flag**. With resolution, it signals authentic storytelling.

---

### Cohort 5: Confusion
**Emotions:** Awkwardness, Boredom, Confusion, Doubt, Embarrassment

**Usage note:** **Always a warning signal.** Significant scores here mean the ad is losing its audience. Investigate what is causing the confusion before running at scale.

---

### Cohort 6: Neutral
**Usage note:** Low engagement states. A warning signal alongside Confusion. An ad that generates primarily Neutral responses is not working.

---

## Demographic Response Patterns

### Young Males 18–34
- **Dominant motivations:** Achievement and Status
- **Responds to:** Positive Adrenaline cohort
- **Attention pattern:** Needs immediate hook in first 3 seconds. Fast cutting acceptable.
- **Credibility signals:** Celebrity and athlete presence
- **Warning:** Value messaging actively hurts resonance for this group unless product is explicitly value-positioned

### Budget-Conscious Audiences
- **Dominant motivation:** Value and Fairness
- **Responds to:** Hope and Relief from Empathy cohort
- **Needs:** Explicit value messaging — free, affordable, accessible framing
- **Warning:** High production values and aspirational settings reduce resonance by creating distance

### Older Affluent Audiences 45+
- **Dominant motivation:** Security and Reliability
- **Responds to:** Empathy cohort — Admiration, Pride, Nostalgia
- **Attention pattern:** Slow pacing, clear narrative, sophisticated production
- **Warning:** Fast cutting and aggressive energy actively repels this group. Trust signals and reliability messaging essential.

---

## Neuroscience Findings Applied in Scoring

1. **The 3-Second Rule:** Emotional signals predict ad liking from the third second of exposure. The opening three seconds determine whether the ad gets emotional processing or is tuned out. The opening hook is always scored as a critical element.

2. **Peak-End Rule:** People remember ads by their most intense emotional moment and how they ended. A strong emotional peak and positive resolution dramatically improves recall and brand association. Ads without a clear peak or a flat ending are penalised.

3. **Active vs Passive Attention:** Active attention — where the viewer has an emotional reaction — is what drives outcomes. Passive viewing alone does not predict conversion. Ads that sustain emotional engagement throughout score higher than ads with isolated moments.

4. **Music as Fast Signal:** Music is one of the fastest emotional signals an ad sends. Tempo and genre communicate audience intent within two seconds. The audio analysis (tempo BPM, energy level, spectral character) is therefore weighted heavily in Dimension 2 and 5 scoring.

---

## Weighted Scoring Formula

When calculating the Overall Resonance Score, dimensions are weighted as follows:

| Dimension | Weight |
|-----------|--------|
| Emotional Power | 30% |
| Emotional Register Match | 25% |
| Identity Signal Fit | 20% |
| Motivational Alignment | 15% |
| Attention Architecture Fit | 10% |

**Formula:** Overall = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)

**Budget concentration tiers:**
- Overall 8.0–10.0: High concentration — primary target for this campaign
- Overall 6.0–7.9: Medium concentration — include with secondary budget weight
- Overall 4.0–5.9: Low concentration — test only, monitor results
- Overall 0–3.9: Deprioritise — do not concentrate spend here
