# Broadlab Creative Intelligence Platform — Claude Code Context

## Before you do anything

If something is unclear, ask. The person you are working with (Greg) has no coding experience — no Python, no React, nothing. Every explanation must be in plain English. Every terminal command must be written out exactly, including the `cd` navigation step first. Never assume Greg knows what a technical term means.

If a task would require changing something that already works, flag it before touching it.

---

## What this is

An internal web tool for Broadlab — a UK-based AI-driven addressable TV advertising company. Campaign team members upload a video ad (MP4), fill in basic campaign context, and the system automatically analyses the ad and produces a **resonance scorecard** — a structured report that predicts which UK audience demographics will respond best to the ad and why.

The output directly informs postcode-level targeting for CTV (connected TV) campaigns across 18 million UK households.

**The core question the system answers:** Which type of person is this ad psychologically built for, and where in the UK do we find the most of those people?

---

## Current build status

The full system is built and running locally. It has been tested against the Nike "Why Do It 2025" ad and produces a complete output. The next step is deploying it so any Broadlab employee can access it via a URL (Railway for backend, Vercel for frontend).

**What works:**
- Full 8-step analysis pipeline runs end to end
- Dashboard UI at http://localhost:5173
- Nike test case button on the dashboard
- Quick Summary and Full Analysis output modes
- PDF download
- Anthropic API key configured
- OpenAI API key configured

**What is not set up yet:**
- AWS Rekognition (not needed — replaced with Claude Vision)
- Railway deployment (in progress)
- Vercel deployment (in progress)
- Snowflake postcode data (future integration)
- DAIVID emotion scores (future integration)

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
├── .env                             ← API keys (never commit this)
├── .gitignore
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
│   │   ├── analyse_frames.py        ← Step 5: Claude Vision analyses frames (replaced AWS)
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

Step 5 uses Claude Vision (not AWS). No AWS account is needed. The only API keys required are Anthropic and OpenAI.

For the Nike test case, Step 5 uses a pre-loaded Rekognition JSON from `test-assets/nike_rekognition.json` instead of Claude Vision, because that file contains richer celebrity detection data.

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

Full methodology is in `framework/RESEARCH_FRAMEWORK.md` and `framework/SCORING_RUBRIC.md`.

---

## API keys and environment variables

All keys live in `.env` in the project root. This file is gitignored — never commit it.

```
ANTHROPIC_API_KEY=        ← configured ✓
OPENAI_API_KEY=           ← configured ✓
AWS_ACCESS_KEY_ID=        ← not needed (Claude Vision replaced Rekognition)
AWS_SECRET_ACCESS_KEY=    ← not needed
AWS_REGION=eu-west-2
AWS_S3_BUCKET=            ← not needed
AWS_REKOGNITION_ROLE_ARN= ← not needed
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

For production deployment (Railway), these are set as environment variables in the Railway dashboard — no `.env` file on the server.

---

## How to run locally

Requires: Node.js, Python 3.9+, FFmpeg (`brew install ffmpeg`)

**Terminal 1 — backend:**
```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/backend"
source venv/bin/activate
python main.py
```

**Terminal 2 — frontend:**
```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/frontend"
npm run dev
```

Then open: http://localhost:5173

---

## Deployment target

- **Backend:** Railway (railway.app) — Python FastAPI server
- **Frontend:** Vercel (vercel.com) — React/Vite app
- **Repo:** https://github.com/gregbrenner27/broadlab-creative-inteligence

Deployment is in progress. When complete, any Broadlab employee will access the tool via a single URL with no local setup required.

---

## Future integrations (not built yet)

| Integration | File | What it adds |
|---|---|---|
| DAIVID API | `future/DAIVID_INTEGRATION.md` | Replaces inferred emotion scores with validated human-response data |
| Broadlab Motivation Graph | `future/MOTIVATION_GRAPH.md` | Replaces generic 5-state motivation framework with Broadlab's proprietary taxonomy |
| Snowflake postcode data | `future/SNOWFLAKE_INTEGRATION.md` | Adds specific UK postcode recommendations to the targeting section |

---

## Key decisions already made — do not reverse without asking

- **Claude Vision replaced AWS Rekognition** — this was intentional. AWS required too much setup for a self-service internal tool. Claude Vision works with just the Anthropic key.
- **claude-sonnet-4-5 is the model** — specified in the original brief. Do not change without asking.
- **max_tokens is 8192 for genome and resonance calls** — was 4096, caused truncated JSON. Do not lower this.
- **Sessions stored in memory** — fine for now, will move to file-based storage before production deployment.
- **No AWS dependency** — the system is designed to work with Anthropic + OpenAI only.
