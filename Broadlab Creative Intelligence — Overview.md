# Broadlab Creative Intelligence Platform
### Internal Tool Overview — May 2026

---

## What This Is

A web-based analysis tool that takes any video ad, breaks it down across five psychological dimensions, and produces a structured report showing which UK audience types the ad will resonate with most — and why.

The goal is to remove the guesswork from creative evaluation. Before a single pound of media spend is committed, the team knows which audiences the ad is genuinely built for, with scored reasoning behind every conclusion.

---

## How It Works

A team member opens the dashboard in their browser, uploads an MP4, and answers five questions about the campaign — brand, category, goal, target audience, and primary motivation. They hit Run Analysis. Within a few minutes they receive a full report.

Under the hood, the system runs eight steps automatically:

1. Extracts and analyses the audio — measuring tempo, energy, and emotional character
2. Transcribes every word spoken in the ad
3. Analyses the visual content of the ad frame by frame
4. Synthesises all of the above into a Creative Genome — a complete psychological profile of the ad
5. Scores the ad against UK audience types across five dimensions
6. Writes a full report in plain English with reasoning behind every score

The output is available as an on-screen report or a downloadable PDF.

---

## The Five Scoring Dimensions

Grounded in DAIVID's 39-emotion framework and System1 advertising effectiveness research.

| Dimension | Weight | What It Measures |
|---|---|---|
| Emotional Power | 30% | How strongly the ad makes you feel something |
| Emotional Register Match | 25% | Whether the emotion triggered is right for this audience |
| Identity Signal Fit | 20% | Whether the audience feels the ad was made for them |
| Motivational Alignment | 15% | Whether the ad's promise matches what drives this audience |
| Attention Architecture Fit | 10% | Whether the pacing matches how this audience's attention works |

Scores run from 0–10. Above 8.0 is high priority. 6.0–7.9 is medium. Below 6.0 is deprioritise.

---

## How This Fits Into Broadlab's Operation

Broadlab's strength is precision targeting — getting the right ad in front of the right household. This tool adds the layer that sits before that decision: **is this ad actually right for that audience?**

It connects creative evaluation directly to targeting strategy. Rather than a gut call on whether an ad suits an audience, the team has a scored, reasoned, research-backed output they can act on and present to clients with confidence.

Long term, once connected to Broadlab's postcode data, the tool completes the loop entirely — from creative analysis to specific UK postcode recommendations in a single workflow.

---

## Current Status

The prototype is fully built and operational. It has been tested end to end against a real campaign (Nike — Why Do It 2025) and produces a complete scored report. The tool runs locally and is ready to be demonstrated.

---

## What Is Needed to Reach Full Capability

The following items are required to move from prototype to production tool.

**From Broadlab:**

| What | Why It's Needed |
|---|---|
| Access to Snowflake postcode data | Converts audience scores into specific UK postcode targeting recommendations — the direct operational output |
| Broadlab's audience segmentation taxonomy | Replaces generic audience types with Broadlab's own definitions, making scores more accurate and internally consistent |
| Broadlab's motivation framework | Replaces the standard motivation model with Broadlab's proprietary one, built from real campaign performance data |
| DAIVID API access | Replaces inferred emotion scores with validated human-response data — significantly increases credibility with clients |
| A real client brief to calibrate against | Needed to validate and fine-tune the scoring methodology against an actual campaign |
| Brand safety and data handling requirements | Determines how client video files are stored, processed, and deleted |

**Infrastructure (handled on the build side):**

| Tool | Purpose | Cost |
|---|---|---|
| Render (Standard) | Hosts the backend server permanently online | $25/month (~£20) |
| Vercel | Hosts the dashboard online | Free |
| GitHub | Code storage and version control | Free |

---

## Cost to Run at Full Capacity

**Per analysis (one ad, full pipeline):**

| Step | Tool | Estimated Cost |
|---|---|---|
| Speech transcription | OpenAI Whisper | ~£0.002 |
| Visual analysis | Claude Vision | ~£0.12–0.16 |
| Creative Genome + Scoring + Report | Claude (Anthropic) | ~£0.10–0.18 |
| **Total per analysis** | | **~£0.25–0.35** |

**Monthly infrastructure:**

| Item | Cost |
|---|---|
| Backend hosting (Render) | ~£20/month |
| AI usage (Anthropic + OpenAI) | Pay per use — see above |
| Everything else | Free |

At 50 analyses per month, total running cost is approximately **£35–40/month** excluding DAIVID, which is enterprise-priced and would need a separate conversation.

---

## Immediate Next Steps

1. Walk through a real client brief together to validate the scoring output
2. Confirm access to Snowflake and DAIVID
3. Align on Broadlab's audience taxonomy and motivation framework
4. Deploy the backend to a permanent server so the tool is always accessible
5. Build the postcode targeting layer once data access is confirmed

---

*Built by Greg Brenner — May 2026*
