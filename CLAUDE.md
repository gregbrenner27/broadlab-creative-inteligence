# Broadlab Creative Intelligence Platform — Claude Code Context

## Before you do anything

If something is unclear, ask. The person you are working with (Greg) has no coding experience — no Python, no React, nothing. Every explanation must be in plain English. Every terminal command must be written out exactly, including the `cd` navigation step first. Never assume Greg knows what a technical term means.

If a task would require changing something that already works, flag it before touching it.

Make all architectural decisions unless Greg specifically asks to choose. Always explain what you are doing and why in plain English before doing it.

---

## Who Greg is

Greg is non-technical — zero experience with Python, React, JavaScript, or any programming. He has just started working at Broadlab and built this prototype before joining. He needs exact terminal commands, plain English explanations, and step-by-step guidance for everything. Never use jargon without explaining it first.

---

## What Broadlab is

Broadlab is a UK-based AI-driven Connected TV (CTV) advertising company. They help brands show video ads to specific households across 18 million UK homes, targeted at postcode level. Their core job is answering: who should see this ad, and where in the UK do those people live?

Broadlab has a campaign planning tool live at `https://campaigns.broadlab.tech/home`. A user enters a company name, industry, budget, KPIs, and an audience brief. Using Broadlab's proprietary postcode and household data, the tool outputs recommended audience personas, media suppliers, and impression volumes for the campaign. The GitHub repo for this tool is `https://github.com/broadlab-tv/audience_builder.git` (private — accessible from Broadlab's systems).

---

## What the Creative Intelligence Platform is

An internal web tool where a team member uploads a video ad (MP4), fills in a short campaign brief, and receives a structured report showing which UK audience types the ad will resonate with most — scored across five psychological dimensions with plain English reasoning behind every score.

**The core question it answers:** Is this creative actually right for the audience we are targeting — and if not, who is it right for?

The output is available on screen or as a downloadable PDF.

---

## Where Creative Intelligence fits into Broadlab's workflow

Broadlab's campaign tool (audience_builder) outputs who to target and where. The Creative Intelligence Platform answers whether the ad itself will resonate with those people.

These are two halves of the same workflow:

1. Brand brings a campaign brief → audience_builder outputs personas and postcodes
2. Brand brings the video ad → Creative Intelligence scores it against those personas
3. If scores are strong, the campaign proceeds with confidence
4. If scores are weak, the creative is adjusted before money is spent

The long-term vision is for these two tools to work together — the persona output from the campaign tool feeds directly into the creative scoring. This is the integration to build toward.

---

## Current build status

The full system is built and tested locally. It has been tested end to end against the Nike "Why Do It 2025" ad and produces a complete scored report. The tool is not yet permanently hosted online — the backend requires manual startup in Terminal.

**What works:**
- Full 8-step analysis pipeline runs end to end
- Dashboard UI at http://localhost:5173
- Nike test case button (one click, no upload needed)
- Quick Summary and Full Analysis output modes
- PDF download
- Anthropic API key configured
- OpenAI API key configured

**What is not yet set up:**
- Permanent backend hosting (Render free tier ran out of memory — needs Standard plan at $25/month or alternative)
- Vercel frontend deployment (configured but backend not live yet)
- Snowflake postcode data connection (future integration)
- DAIVID emotion score API (future integration)
- Integration with audience_builder persona output

---

## Feature roadmap — build in this order

| Priority | Feature | What it does | Effort |
|---|---|---|---|
| 1 | Plain English reasoning on every score | Every score includes 2–3 sentences explaining exactly why that number was given | Low — prompt update only |
| 2 | "Who is this report for?" setting | User selects: Internal Team, Client Presentation, Media Planning, or Executive Summary. Claude adjusts language and detail accordingly | Low — one form field, one prompt update |
| 3 | Frames every 2 seconds instead of 6 | Triples visual coverage of the ad. Quick improvement to visual analysis accuracy | Very low — one number changes |
| 4 | Full video input to Claude | Send the entire MP4 to Claude instead of extracted frames. Claude watches the full ad. Removes the frame limitation entirely | Medium — replaces pipeline steps 4 and 5 |
| 5 | Confidence indicator on each score | Flags High / Medium / Needs Human Review on each score based on data quality available | Medium |
| 6 | Post-report chatbot | After the report, user can ask follow-up questions. Claude only answers what it can ground in the report — refuses to speculate | Medium-high |
| 7 | Side-by-side ad comparison | Analyse multiple creatives simultaneously and compare scores | High |
| 8 | UK postcode targeting layer | Connect to Broadlab's Snowflake data to output specific postcode recommendations matching top-scoring audiences | High — requires Snowflake access from Broadlab |
| 9 | Integration with audience_builder | Persona output from Broadlab's campaign tool feeds directly into Creative Intelligence scoring | High — requires access to audience_builder repo and data |

---

## Known limitations and planned fixes

**Visual analysis gap:** Claude currently only sees a still frame every 6 seconds. For a 30-second ad that is 5 images. Fast cuts, short product reveals, and key visual moments can be missed entirely.

- Quick fix: increase to 1 frame every 2 seconds (Feature 3 above)
- Proper fix: send the full MP4 directly to Claude so it watches the entire video (Feature 4 above)

---

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18 + Tailwind CSS | The dashboard interface |
| Backend | Python FastAPI | The API server |
| AI synthesis | Anthropic Claude (claude-sonnet-4-5) | Creative Genome, resonance scoring, final report |
| Speech transcription | OpenAI Whisper API | Transcribes speech from the ad |
| Visual analysis | Claude Vision (frame analysis) | Replaced AWS Rekognition — no AWS needed |
| Audio analysis | Librosa (Python library) | Tempo, energy, spectral features |
| Frame extraction | FFmpeg (command line tool) | Pulls JPEG frames from the MP4 |
| PDF generation | ReportLab (Python library) | Generates the downloadable PDF report |
| Build tool | Vite | Compiles the React frontend |

---

## Design system

Match this exactly for all UI work:

- Background: `#0d0d0d` (very dark, near black)
- Card/panel background: `#1a1a1a`
- Border colour: `#2a2a2a`
- Primary text: `#ffffff`
- Secondary text: `#a0a0a0`
- Accent colour: `#e63946` (red — buttons, highlights, scores)
- Font: Inter (loaded from Google Fonts)
- Style: Minimal, data-forward, premium internal tool feel
- Reference site: https://broad-lab-rework.vercel.app/

Tailwind custom colours are configured in `frontend/tailwind.config.js` under the `broadlab` key.

---

## Project file structure

```
broadlab-creative-intelligence/
├── CLAUDE.md                        ← this file
├── README.md                        ← setup instructions for humans
├── Broadlab Creative Intelligence — Overview.md  ← one-page summary for sharing with the team
├── .env                             ← API keys (never commit this)
├── .gitignore
├── render.yaml                      ← Render deployment config (backend hosting)
│
├── framework/                       ← research methodology (read-only reference)
│   ├── RESEARCH_FRAMEWORK.md        ← the 5 scoring dimensions, DAIVID cohorts, demographic patterns
│   ├── SCORING_RUBRIC.md            ← how Claude scores each dimension
│   ├── PERSONA_TEMPLATE.md          ← persona schemas and pre-built personas
│   └── OUTPUT_TEMPLATE.md           ← JSON schemas for genome, scorecard, report
│
├── prompts/                         ← AI prompts used in every Claude API call
│   ├── SYSTEM_PROMPT.md             ← Claude's role and baseline rules
│   ├── GENOME_PROMPT.md             ← instructions for generating the Creative Genome
│   ├── RESONANCE_PROMPT.md          ← instructions for scoring resonance
│   └── SYNTHESIS_PROMPT.md          ← instructions for producing the final report
│
├── future/                          ← placeholders for upcoming integrations
│   ├── DAIVID_INTEGRATION.md
│   ├── MOTIVATION_GRAPH.md
│   └── SNOWFLAKE_INTEGRATION.md
│
├── test-assets/                     ← Nike test case files
│   ├── nike_ad.mp4                  ← excluded from git (too large)
│   └── nike_rekognition.json        ← pre-loaded Rekognition data for Nike test
│
├── backend/
│   ├── main.py                      ← FastAPI server, all API endpoints, pipeline orchestrator
│   ├── generate_pdf.py              ← ReportLab PDF generation
│   ├── requirements.txt             ← Python dependencies
│   ├── temp/                        ← created at runtime, excluded from git
│   │
│   ├── pipeline/                    ← one file per pipeline step
│   │   ├── extract_audio.py         ← Step 1: FFmpeg extracts WAV from MP4
│   │   ├── analyse_audio.py         ← Step 2: Librosa analyses tempo/energy/spectral
│   │   ├── transcribe.py            ← Step 3: OpenAI Whisper transcribes speech
│   │   ├── extract_frames.py        ← Step 4: FFmpeg extracts JPEG frames every 6s
│   │   ├── analyse_frames.py        ← Step 5: Claude Vision analyses frames
│   │   └── run_rekognition.py       ← legacy AWS step + file loader for Nike test JSON
│   │
│   └── claude/                      ← three Claude API synthesis calls
│       ├── genome_call.py           ← Step 6: produces genome.json
│       ├── resonance_call.py        ← Step 7: produces scorecard.json
│       └── synthesis_call.py        ← Step 8: produces report.json (3 formats)
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── tailwind.config.js
    ├── vite.config.js               ← proxies /api to localhost:8000 in dev
    └── src/
        ├── main.jsx                 ← React entry point
        ├── App.jsx                  ← routing (/ = Dashboard, /results/:id = Results)
        ├── index.css                ← Tailwind + global styles
        ├── assets/                  ← logo and static images
        ├── components/
        │   ├── UploadPanel.jsx      ← drag-and-drop MP4 upload
        │   ├── InputForm.jsx        ← campaign context + audience + output mode
        │   ├── AnalysisProgress.jsx ← 8-step live progress indicator (SSE)
        │   ├── QuickSummary.jsx     ← single-card results view
        │   ├── FullAnalysis.jsx     ← tabbed results view (4 tabs)
        │   └── PDFDownload.jsx      ← triggers PDF download from backend
        └── pages/
            ├── Dashboard.jsx        ← Screen 1: upload + form + Nike test button
            └── Results.jsx          ← Screen 2: progress + results display
```

---

## The 8-step pipeline

Every time an analysis runs, these steps execute in sequence. Progress is streamed to the frontend in real time via Server-Sent Events (SSE).

| Step | File | What it does |
|---|---|---|
| 1 | `extract_audio.py` | FFmpeg pulls audio from MP4 → saves as WAV |
| 2 | `analyse_audio.py` | Librosa extracts tempo (BPM), energy (RMS), spectral character |
| 3 | `transcribe.py` | OpenAI Whisper converts speech to text with timestamps |
| 4 | `extract_frames.py` | FFmpeg saves 1 JPEG frame every 6 seconds |
| 5 | `analyse_frames.py` | Claude Vision looks at frames and describes visuals |
| 6 | `genome_call.py` | Claude synthesises all inputs into a Creative Genome JSON |
| 7 | `resonance_call.py` | Claude scores the ad against the target persona (5 dimensions) |
| 8 | `synthesis_call.py` | Claude produces Quick Summary + Full Analysis + PDF content |

For the Nike test case, Step 5 uses a pre-loaded Rekognition JSON from `test-assets/nike_rekognition.json` instead of Claude Vision.

---

## The 5 scoring dimensions

Every ad is scored 0–10 for each audience persona across these dimensions, with weighted overall score:

| Dimension | Weight | What it measures |
|---|---|---|
| Emotional Power | 30% | How strongly the ad makes people feel something |
| Emotional Register Match | 25% | Whether the emotional cohort matches what this audience responds to |
| Identity Signal Fit | 20% | Whether visual signals make the audience feel the ad is for them |
| Motivational Alignment | 15% | Whether the ad's promise matches the audience's core driver |
| Attention Architecture Fit | 10% | Whether pacing and structure matches how this audience's attention works |

Overall = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)

Budget concentration tiers: 8.0–10.0 = High, 6.0–7.9 = Medium, 4.0–5.9 = Low, 0–3.9 = Deprioritise

Grounded in DAIVID's 39-emotion framework and System1 advertising effectiveness research.

Full methodology is in `framework/RESEARCH_FRAMEWORK.md` and `framework/SCORING_RUBRIC.md`.

---

## API keys and environment variables

All keys live in `.env` in the project root. This file is gitignored — never commit it.

```
ANTHROPIC_API_KEY=        ← configured ✓
OPENAI_API_KEY=           ← configured ✓
AWS_ACCESS_KEY_ID=        ← not needed (Claude Vision replaced Rekognition)
AWS_SECRET_ACCESS_KEY=    ← not needed
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

For production deployment, these are set as environment variables in the hosting dashboard — no `.env` file on the server.

---

## How to run locally

Requires: Node.js, Python 3.9+, FFmpeg

**Terminal 1 — backend (start this first, wait for it to finish loading):**
```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/backend" && source venv/bin/activate && python main.py
```
Wait until you see: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 — frontend:**
```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/frontend" && npm run dev
```
Wait until you see: `Local: http://localhost:5173`

Then open: http://localhost:5173

Keep both Terminal windows open. Closing either one stops that half of the tool.

Note: the file paths above are for Greg's personal Mac. On a new computer the paths will be different — update them to wherever the repo was cloned.

---

## Deployment

- **Frontend:** Vercel (vercel.com) — configured, deploys automatically on git push
- **Backend:** Render (render.com) — render.yaml is configured. Free tier ran out of memory (512MB limit exceeded by heavy Python libraries). Needs Standard plan ($25/month, 2GB RAM) to run reliably.
- **Repo:** https://github.com/gregbrenner27/broadlab-creative-inteligence

---

## What Broadlab needs to provide for full capability

| What | Why |
|---|---|
| Access to Snowflake postcode data | To output specific UK postcode recommendations |
| Audience segmentation taxonomy | To replace generic audience types with Broadlab's own |
| Motivation framework | Proprietary version built from Broadlab's campaign data |
| DAIVID API access | To replace inferred emotion scores with validated human-response data |
| Access to audience_builder repo | To understand persona structure and build the integration |
| A real client brief to test against | To validate and calibrate scoring against an actual campaign |

---

## Key decisions already made — do not reverse without asking

- **Claude Vision replaced AWS Rekognition** — intentional. AWS required too much setup. Claude Vision works with just the Anthropic key.
- **claude-sonnet-4-5 is the model** — do not change without asking.
- **max_tokens is 8192 for genome and resonance calls** — was 4096, caused truncated JSON. Do not lower this.
- **Sessions stored in memory** — fine for now, will move to file-based storage before production.
- **No AWS dependency** — system is designed to work with Anthropic + OpenAI only.
