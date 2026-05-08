# Broadlab Creative Intelligence Platform

An internal AI tool that analyses video ad creatives and produces resonance scorecards — predicting which UK audience demographics will respond best to each ad.

## What It Does

Upload an MP4 ad. Fill in brand and campaign details. The system automatically:
1. Extracts and analyses the audio (tempo, energy, emotional register)
2. Transcribes the speech
3. Extracts visual frames for analysis
4. Runs AWS Rekognition for visual AI detection
5. Synthesises everything with Claude AI into a structured Creative Genome
6. Scores the ad against your target audience across 5 dimensions
7. Produces a targeting recommendation and optional PDF report

## Setup — One-Time Steps

### 1. Install Prerequisites

You need three things installed on your Mac before starting:

**Node.js** (runs the frontend): https://nodejs.org — download the LTS version and install it.

**Python 3.11+** (runs the backend): https://python.org/downloads — download and install.

**FFmpeg** (video processing tool): Open Terminal and paste:
```
brew install ffmpeg
```
If brew isn't installed, first run:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Add Your API Keys

Open the `.env` file in this folder and replace each `your_xxx_here` placeholder with your actual keys.

### 3. Set Up the Backend

Open Terminal. Type these commands one at a time, pressing Enter after each:

```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/backend"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Set Up the Frontend

Open a second Terminal window. Type:

```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/frontend"
npm install
```

## Running the App

Every time you want to use the app, you need two Terminal windows running simultaneously.

**Terminal 1 — Backend:**
```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/backend"
source venv/bin/activate
python main.py
```

**Terminal 2 — Frontend:**
```bash
cd "/Users/gregbrenner/creative inteligence (broadlab)/broadlab-creative-intelligence/frontend"
npm run dev
```

Then open your browser and go to: **http://localhost:5173**

## Project Structure

```
broadlab-creative-intelligence/
├── .env                    ← Your API keys (never share this)
├── framework/              ← Research methodology and scoring rubric
├── prompts/                ← AI prompts for Claude
├── future/                 ← Placeholders for upcoming integrations
├── backend/                ← Python server and analysis pipeline
│   ├── main.py             ← API server entry point
│   ├── pipeline/           ← Each analysis step as a separate file
│   └── claude/             ← Claude AI synthesis calls
└── frontend/               ← React web interface
    └── src/
        ├── components/     ← Reusable UI pieces
        └── pages/          ← Full page layouts
```
