# Broadlab Creative Intelligence — Output Template

This file defines the exact JSON schemas that every Claude API call must produce. The backend validates responses against these schemas before passing them to the next pipeline step.

---

## Schema 1: Creative Genome (genome.json)

Produced by: `genome_call.py`  
Used by: `resonance_call.py`, `synthesis_call.py`

```json
{
  "genome": {
    "ad_title": "string — brand and campaign name if identifiable",
    "duration_seconds": "number",
    
    "visual_profile": {
      "dominant_subjects": ["array of main subjects detected e.g. athletes, cars, families"],
      "setting": "string — where the ad takes place",
      "colour_palette": "string — warm/cool/neutral/high-contrast/monochrome etc.",
      "pacing": "string — slow/medium/fast/very fast",
      "production_quality": "string — lo-fi/standard/high/cinematic",
      "casting_signals": "string — who is in the ad and what it implies about the intended audience",
      "celebrity_presence": "boolean",
      "celebrities_detected": ["array of celebrity names if any"],
      "identity_signal_summary": "string — one paragraph on what the visual signals say about the intended audience"
    },
    
    "audio_profile": {
      "tempo_bpm": "number",
      "energy_level": "string — low/medium/high/very high",
      "spectral_character": "string — bright/dark/warm/harsh",
      "dominant_genre": "string — e.g. hip-hop, orchestral, electronic, acoustic pop",
      "emotional_register_of_music": "string — e.g. triumphant, melancholic, energetic, calm",
      "music_daivid_cohort": "string — which DAIVID cohort the music most strongly activates"
    },
    
    "speech_profile": {
      "has_voiceover": "boolean",
      "has_dialogue": "boolean",
      "transcript_summary": "string — key phrases and messages from the speech",
      "language_register": "string — e.g. aspirational, functional, inclusive, urgent, poetic",
      "cta_present": "boolean",
      "cta_text": "string — the actual call to action if present",
      "key_messages": ["array of the 3 most important messages in the transcript"]
    },
    
    "emotional_arc": {
      "opening_hook": "string — what happens in the first 3 seconds",
      "hook_strength": "string — weak/moderate/strong/very strong",
      "dominant_emotion_journey": "string — describe the emotional journey from start to finish",
      "peak_moment": "string — the single most emotionally intense moment",
      "resolution": "string — how the ad ends emotionally",
      "peak_end_quality": "string — weak/moderate/strong — assessment of peak moment and ending combined"
    },
    
    "daivid_classification": {
      "dominant_cohort": "string — the primary DAIVID cohort",
      "secondary_cohort": "string or null",
      "warning_cohorts_present": ["any Confusion or unresolved Negative Adrenaline flags"],
      "cohort_reasoning": "string — why these cohorts were assigned based on the data"
    },
    
    "motivational_promise": {
      "primary_promise": "string — what the ad says the product will do for you",
      "motivation_category": "string — Achievement/Belonging/Security/Status/Value",
      "promise_clarity": "string — weak/moderate/strong"
    },
    
    "attention_architecture": {
      "hook_timing_seconds": "number — when does the first emotional hook occur",
      "cuts_per_minute": "number — estimated",
      "narrative_structure": "string — linear/fragmented/montage/problem-solution/emotional journey",
      "information_density": "string — low/medium/high",
      "complexity": "string — simple/moderate/complex"
    }
  }
}
```

---

## Schema 2: Resonance Scorecard (scorecard.json)

Produced by: `resonance_call.py`  
Used by: `synthesis_call.py`

```json
{
  "scorecard": {
    "persona": {
      "name": "string",
      "description": "string",
      "primary_motivation": "string"
    },
    
    "dimension_scores": {
      "emotional_power": {
        "score": "number 0-10",
        "reasoning": "string — 2-3 sentences citing specific genome data"
      },
      "emotional_register_match": {
        "score": "number 0-10",
        "reasoning": "string"
      },
      "identity_signal_fit": {
        "score": "number 0-10",
        "reasoning": "string"
      },
      "motivational_alignment": {
        "score": "number 0-10",
        "reasoning": "string"
      },
      "attention_architecture_fit": {
        "score": "number 0-10",
        "reasoning": "string"
      }
    },
    
    "overall_resonance_score": "number — weighted average per formula in RESEARCH_FRAMEWORK.md",
    
    "strengths": [
      "string — strength 1 with specific evidence",
      "string — strength 2 with specific evidence",
      "string — strength 3 with specific evidence"
    ],
    
    "gaps": [
      "string — gap 1 as an actionable observation",
      "string — gap 2 as an actionable observation"
    ],
    
    "budget_concentration": "string — High / Medium / Low / Deprioritise",
    "budget_concentration_rationale": "string — one sentence explanation"
  }
}
```

---

## Schema 3: Final Synthesis Report (report.json)

Produced by: `synthesis_call.py`  
Used by: frontend display and PDF generation

```json
{
  "report": {
    "quick_summary": {
      "verdict": "string — one sentence overall verdict",
      "overall_score": "number",
      "top_recommended_audience": "string",
      "three_strengths": ["string", "string", "string"],
      "two_critical_gaps": ["string", "string"],
      "targeting_recommendation": "string — plain English recommendation"
    },
    
    "full_analysis": {
      "overall_verdict": "string",
      "overall_score": "number",
      
      "creative_genome_narrative": "string — multi-paragraph narrative of what the ad is doing",
      
      "daivid_cohort_analysis": {
        "dominant_cohort": "string",
        "cohort_meaning": "string — what this cohort means for audience fit",
        "secondary_signals": "string"
      },
      
      "persona_scorecards": [
        {
          "persona_name": "string",
          "overall_score": "number",
          "dimension_scores": {
            "emotional_power": "number",
            "emotional_register_match": "number",
            "identity_signal_fit": "number",
            "motivational_alignment": "number",
            "attention_architecture_fit": "number"
          },
          "dimension_reasoning": {
            "emotional_power": "string",
            "emotional_register_match": "string",
            "identity_signal_fit": "string",
            "motivational_alignment": "string",
            "attention_architecture_fit": "string"
          },
          "strengths": ["string", "string", "string"],
          "gaps": ["string", "string"],
          "budget_concentration": "string",
          "budget_concentration_rationale": "string"
        }
      ],
      
      "targeting_recommendation": {
        "primary_target": "string — audience to concentrate primary budget on",
        "secondary_target": "string or null",
        "deprioritise": "string — audiences to avoid",
        "reasoning": "string — multi-sentence explanation",
        "postcode_note": "string — how this maps to UK postcode clusters when Snowflake data is available"
      },
      
      "creative_flags": {
        "working_well": ["string", "string", "string"],
        "not_working": ["string", "string"],
        "improvement_recommendations": ["string", "string"]
      },
      
      "future_integration_note": "string — where DAIVID and Snowflake data will enhance this analysis"
    },
    
    "pdf_content": "string — the full analysis written in clean professional prose, no JSON formatting, suitable for internal presentation or client sharing"
  }
}
```
