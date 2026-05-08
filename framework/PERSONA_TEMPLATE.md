# Broadlab Creative Intelligence — Persona Template

When a user describes a target audience, the system structures it into a standard persona format before passing it to Claude for resonance scoring. This template defines that structure.

---

## Persona Schema

```json
{
  "persona_id": "unique identifier e.g. persona_1",
  "name": "short descriptive label e.g. Young Competitive Males",
  "description": "the user's plain English description of this audience",
  "age_range": "e.g. 18-34",
  "primary_motivation": "one of: Achievement, Belonging, Security, Status, Value",
  "secondary_motivation": "optional — one of the five motivations above",
  "daivid_cohort_affinity": "the DAIVID cohort most likely to resonate — see RESEARCH_FRAMEWORK.md",
  "attention_profile": "Short / Medium / Long — how much patience this audience has",
  "identity_signals": ["list", "of", "signals", "this", "audience", "looks", "for"],
  "red_flags": ["creative choices", "that", "actively repel", "this audience"]
}
```

---

## Pre-Built Personas

The following personas are available as defaults and can be selected from the UI. They can be modified or supplemented with user-provided descriptions.

### Persona: Young Competitive Males
```json
{
  "persona_id": "persona_ycm",
  "name": "Young Competitive Males",
  "description": "Men aged 18–34 who identify strongly with sport, competition, and achievement. Gaming, football, fitness, and betting are common contexts.",
  "age_range": "18-34",
  "primary_motivation": "Achievement",
  "secondary_motivation": "Status",
  "daivid_cohort_affinity": "Positive Adrenaline",
  "attention_profile": "Short",
  "identity_signals": ["athletes", "competitive settings", "winning moments", "male peer groups", "fast energy", "bold typography"],
  "red_flags": ["value messaging", "slow pacing", "family settings", "female-dominant casting without context", "overly aspirational luxury"]
}
```

### Persona: Budget-Conscious Families
```json
{
  "persona_id": "persona_bcf",
  "name": "Budget-Conscious Families",
  "description": "Households managing finances carefully. Motivated by getting genuine value. Often have children. Practical rather than aspirational.",
  "age_range": "25-45",
  "primary_motivation": "Value",
  "secondary_motivation": "Belonging",
  "daivid_cohort_affinity": "Empathy",
  "attention_profile": "Medium",
  "identity_signals": ["real family moments", "everyday settings", "price/value framing", "inclusive language", "warm but practical tone"],
  "red_flags": ["luxury settings", "high production gloss", "status messaging", "celebrity without value context", "exclusive or premium positioning"]
}
```

### Persona: Older Affluent Professionals
```json
{
  "persona_id": "persona_oap",
  "name": "Older Affluent Professionals",
  "description": "Adults 45+ with disposable income and established preferences. Value quality, trust, and reliability. Sceptical of hype. Respond to substance over style.",
  "age_range": "45-65",
  "primary_motivation": "Security",
  "secondary_motivation": "Status",
  "daivid_cohort_affinity": "Empathy",
  "attention_profile": "Long",
  "identity_signals": ["quality craftsmanship", "calm confident pacing", "clear narrative", "trusted voiceover", "sophisticated settings", "heritage signals"],
  "red_flags": ["aggressive energy", "fast cutting", "youth-coded music", "urgency tactics", "complexity without clarity"]
}
```

### Persona: Aspiration-Driven Young Adults
```json
{
  "persona_id": "persona_adya",
  "name": "Aspiration-Driven Young Adults",
  "description": "People in their mid-20s to mid-30s motivated by self-improvement, lifestyle elevation, and being seen as successful. Mix of genders. Career and aesthetics matter.",
  "age_range": "24-35",
  "primary_motivation": "Status",
  "secondary_motivation": "Achievement",
  "daivid_cohort_affinity": "Approach",
  "attention_profile": "Short",
  "identity_signals": ["beautiful production", "aspirational settings", "lifestyle imagery", "confident protagonists", "clean aesthetic", "effortless success"],
  "red_flags": ["budget framing", "mundane settings", "excessive humour that undermines aspiration", "too much text on screen"]
}
```

---

## How Personas Are Used

1. The user describes their target audience in plain English in the Input Form.
2. The user selects a Primary Motivation from the dropdown.
3. The backend maps this to the closest pre-built persona or constructs a custom one using the schema above.
4. The persona JSON is passed to `resonance_call.py` alongside the Creative Genome.
5. Claude scores the ad against this persona using SCORING_RUBRIC.md.
