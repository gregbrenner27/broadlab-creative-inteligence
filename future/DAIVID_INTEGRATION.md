# Future Integration: DAIVID API

## What DAIVID Is

DAIVID is a creative effectiveness platform that scores ads across 39 emotions using AI trained on tens of millions of human responses. It produces validated, human-calibrated emotion scores for any video ad, telling you with high confidence how audiences emotionally respond moment by moment.

## Why This Integration Matters

Currently, the Creative Intelligence Platform approximates emotional register using Claude's interpretation of Rekognition visual data, Librosa audio features, and the speech transcript. This is effective but inferential — Claude is reasoning about what emotions the ad is likely to trigger, not measuring actual human emotional responses.

When DAIVID API access is available, the platform will replace this approximation with validated DAIVID emotion scores. This significantly improves the accuracy of:
- **Dimension 2 (Emotional Register Match)** — currently the weakest dimension due to inference limitations
- **DAIVID Cohort Classification** in the Creative Genome — will be data-driven rather than model-inferred
- **Peak-End Rule assessment** — DAIVID provides moment-by-moment scores, making peak detection precise

## Where to Insert the API Call

Insert the DAIVID API call between **Step 5 (run_rekognition.py)** and **Step 6 (genome_call.py)** in the pipeline.

```
Step 5 — run_rekognition.py       [existing]
Step 5b — run_daivid.py           [ADD THIS]
Step 6 — genome_call.py           [existing — update prompt to include DAIVID data]
```

## New File: backend/pipeline/run_daivid.py

When implementing, this file should:
1. Send the MP4 video to the DAIVID API endpoint
2. Poll for completion (DAIVID analysis is typically asynchronous)
3. Retrieve the response: 39 emotion scores with timestamps, cohort breakdown, peak moments
4. Save as `daivid_scores.json` in the temp folder
5. Pass this file to `genome_call.py` as an additional input

## Update Required: genome_call.py

When DAIVID data is available, update the genome prompt to:
- Replace "estimated DAIVID cohort" language with "DAIVID-validated cohort"
- Include the actual emotion scores as evidence in the cohort classification
- Use the moment-by-moment peak data for the emotional arc section

## DAIVID API Documentation

*[Paste DAIVID API endpoint, authentication method, and request/response format here when credentials are obtained.]*

## Contact

DAIVID integration is being coordinated by the Broadlab technology team. When API credentials are available, pass them to the development team to complete this integration.
