"""
main.py
-------
The backend API server for the Broadlab Creative Intelligence Platform.

This is the entry point for the entire backend system. It:
1. Creates a FastAPI web server (FastAPI is a Python framework for building APIs)
2. Defines the API endpoints that the frontend calls
3. Orchestrates the full 8-step analysis pipeline
4. Returns results to the frontend in real-time via Server-Sent Events (SSE)
   — SSE is a technique that lets the server push updates to the browser
     without the browser having to repeatedly ask "are you done yet?"

To run this server: python main.py
Then the API is available at: http://localhost:8000
"""

import os
import uuid
import json
import asyncio
import logging
import shutil
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import all pipeline steps
from pipeline.extract_audio import extract_audio
from pipeline.analyse_audio import analyse_audio
from pipeline.transcribe import transcribe_audio
from pipeline.extract_frames import extract_frames
from pipeline.analyse_frames import analyse_frames_with_claude
from pipeline.run_rekognition import load_rekognition_from_file
from claude.genome_call import generate_creative_genome
from claude.resonance_call import score_resonance
from claude.synthesis_call import generate_final_report

# Import PDF generator
from generate_pdf import create_pdf_report

# ---- SETUP ----

# Load API keys from the .env file in the project root
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Configure logging so we can see what's happening in the terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Read API keys and config from environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")
REKOGNITION_ROLE_ARN = os.getenv("AWS_REKOGNITION_ROLE_ARN")
BACKEND_PORT = int(os.getenv("PORT", os.getenv("BACKEND_PORT", "8000")))

# Temp directory where pipeline files are stored during analysis
TEMP_BASE_DIR = Path(__file__).parent / "temp"
TEMP_BASE_DIR.mkdir(exist_ok=True)

# ---- FASTAPI APP ----

# Create the FastAPI app instance
app = FastAPI(
    title="Broadlab Creative Intelligence API",
    description="Analyses video ad creatives and produces resonance scorecards",
    version="1.0.0"
)

# CORS middleware — allows the React frontend (running on port 5173) to
# call this API (running on port 8000) without being blocked by the browser's
# security rules (CORS = Cross-Origin Resource Sharing)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]
# Allow any Vercel preview/production URL — set FRONTEND_URL in Railway/Render env vars
# to lock it down to a specific domain once deployed
FRONTEND_URL = os.getenv("FRONTEND_URL", "")
if FRONTEND_URL:
    ALLOWED_ORIGINS.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",  # allows all Vercel domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- ACTIVE ANALYSIS SESSIONS ----
# We store in-progress analysis sessions here so the frontend can poll for progress
# In production, this would be a database, but in-memory is fine for local use
active_sessions: dict = {}


# Path to the test assets folder (Nike ad + pre-loaded Rekognition JSON)
TEST_ASSETS_DIR = Path(__file__).parent.parent / "test-assets"


# ---- API ENDPOINTS ----

@app.get("/health")
async def health_check():
    """Simple health check — confirms the server is running."""
    return {"status": "ok", "service": "Broadlab Creative Intelligence"}


@app.post("/api/test-nike")
async def start_nike_test():
    """
    Kick off the Nike test case using the pre-loaded files in test-assets/.
    Uses the pre-existing Rekognition JSON for visual data (faster and more detailed).
    Falls back to Claude Vision if the JSON is not present.
    """
    nike_mp4 = TEST_ASSETS_DIR / "nike_ad.mp4"
    nike_rekognition = TEST_ASSETS_DIR / "nike_rekognition.json"

    if not nike_mp4.exists():
        raise HTTPException(status_code=404, detail=f"Nike MP4 not found at {nike_mp4}")

    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
        raise HTTPException(status_code=500, detail="Anthropic API key not configured in .env")

    session_id = str(uuid.uuid4())
    session_dir = TEMP_BASE_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    # Copy the Nike MP4 into the session directory
    import shutil
    shutil.copy(str(nike_mp4), str(session_dir / "ad.mp4"))

    brand_context = {
        "brand_name": "Nike",
        "category": "Sportswear",
        "campaign_goal": "Drive brand association with athletic achievement and competition",
        "target_audience": "Young adult sports enthusiasts aged 18 to 34 who identify as athletic and competitive",
        "primary_motivation": "Achievement",
        "additional_context": "Nike Why Do It 2025 campaign",
        "secondary_audience": ""
    }

    active_sessions[session_id] = {
        "status": "queued",
        "progress": [],
        "result": None,
        "error": None
    }

    # Use pre-existing Rekognition JSON if available (richer data), else Claude Vision
    rekog_path = str(nike_rekognition) if nike_rekognition.exists() else None

    asyncio.create_task(
        run_analysis_pipeline(
            session_id=session_id,
            video_path=str(session_dir / "ad.mp4"),
            session_dir=str(session_dir),
            brand_context=brand_context,
            output_mode="both",
            rekognition_json_path=rekog_path
        )
    )

    return {"session_id": session_id}


@app.post("/api/analyse")
async def start_analysis(
    video: UploadFile = File(...),           # the uploaded MP4 file
    brand_name: str = Form(...),             # required
    category: str = Form(...),               # required
    campaign_goal: str = Form(...),          # required
    target_audience: str = Form(...),        # required
    primary_motivation: str = Form(...),     # required
    additional_context: str = Form(""),      # optional
    secondary_audience: str = Form(""),      # optional
    output_mode: str = Form("both"),         # "quick", "full", or "both"
    rekognition_json_path: str = Form("")    # optional: pre-loaded Rekognition JSON for testing
):
    """
    Start a new analysis job.

    The frontend sends the video file and all form data here.
    This endpoint saves the video, creates a session, and returns a session ID.
    The frontend then connects to /api/progress/{session_id} to receive live updates.
    """

    # Validate that a video was actually uploaded
    if not video.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 files are accepted")

    # Validate required API keys are present
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="Anthropic API key not configured. Add it to your .env file."
        )

    # Create a unique session ID for this analysis run
    # (uuid4 generates a random unique identifier like "a1b2c3d4-...")
    session_id = str(uuid.uuid4())
    session_dir = TEMP_BASE_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    # Save the uploaded video to the session directory
    video_path = session_dir / "ad.mp4"
    with open(video_path, "wb") as f:
        content = await video.read()
        f.write(content)

    logger.info(f"Session {session_id}: Video saved ({len(content)} bytes)")

    # Package all the user's form inputs together
    brand_context = {
        "brand_name": brand_name,
        "category": category,
        "campaign_goal": campaign_goal,
        "target_audience": target_audience,
        "primary_motivation": primary_motivation,
        "additional_context": additional_context,
        "secondary_audience": secondary_audience
    }

    # Register the session as "queued"
    active_sessions[session_id] = {
        "status": "queued",
        "progress": [],
        "result": None,
        "error": None
    }

    # Start the analysis pipeline in the background
    # asyncio.create_task runs it without blocking this response
    asyncio.create_task(
        run_analysis_pipeline(
            session_id=session_id,
            video_path=str(video_path),
            session_dir=str(session_dir),
            brand_context=brand_context,
            output_mode=output_mode,
            rekognition_json_path=rekognition_json_path if rekognition_json_path else None
        )
    )

    return {"session_id": session_id}


@app.get("/api/progress/{session_id}")
async def get_progress(session_id: str):
    """
    Stream real-time progress updates for an analysis session.

    Uses Server-Sent Events (SSE) — the browser connects once and the server
    pushes updates as each pipeline step completes. The frontend uses this
    to light up the progress indicators.
    """

    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generator that yields SSE-formatted events."""
        last_index = 0

        while True:
            session = active_sessions.get(session_id)
            if not session:
                break

            # Send any new progress events
            events = session["progress"]
            while last_index < len(events):
                event = events[last_index]
                # SSE format: "data: {json}\n\n"
                yield f"data: {json.dumps(event)}\n\n"
                last_index += 1

            # Check if the analysis is complete
            if session["status"] in ("complete", "error"):
                # Send the final status event
                final_event = {
                    "type": "complete" if session["status"] == "complete" else "error",
                    "result": session.get("result"),
                    "error": session.get("error")
                }
                yield f"data: {json.dumps(final_event)}\n\n"
                break

            # Wait briefly before checking again
            await asyncio.sleep(0.5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"  # prevents nginx from buffering SSE
        }
    )


@app.get("/api/result/{session_id}")
async def get_result(session_id: str):
    """Retrieve the completed analysis result for a session."""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]
    if session["status"] != "complete":
        raise HTTPException(status_code=202, detail="Analysis still in progress")

    return session["result"]


@app.get("/api/pdf/{session_id}")
async def download_pdf(session_id: str):
    """Generate and download the PDF report for a completed session."""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]
    if session["status"] != "complete" or not session.get("result"):
        raise HTTPException(status_code=400, detail="No completed result to generate PDF from")

    session_dir = TEMP_BASE_DIR / session_id
    pdf_path = str(session_dir / "report.pdf")

    # Generate the PDF from the report data
    try:
        report_data = session["result"]
        brand_name = session.get("brand_name", "Unknown Brand")
        create_pdf_report(report_data, pdf_path, brand_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"broadlab_analysis_{session_id[:8]}.pdf"
    )


# ---- PIPELINE ORCHESTRATOR ----

async def run_analysis_pipeline(
    session_id: str,
    video_path: str,
    session_dir: str,
    brand_context: dict,
    output_mode: str,
    rekognition_json_path: str = None
):
    """
    Orchestrates all 8 pipeline steps in sequence.
    Updates the session progress dict as each step completes.
    This runs as a background task.
    """

    def push_progress(step: str, status: str, message: str = ""):
        """Add a progress event to the session."""
        event = {"step": step, "status": status, "message": message}
        active_sessions[session_id]["progress"].append(event)
        logger.info(f"Session {session_id}: [{step}] {status} — {message}")

    def store_brand_name():
        """Store brand name for PDF filename generation."""
        active_sessions[session_id]["brand_name"] = brand_context.get("brand_name", "Unknown")

    try:
        store_brand_name()
        active_sessions[session_id]["status"] = "running"

        # ---- STEP 1: Extract Audio ----
        push_progress("extract_audio", "running", "Extracting audio track from video...")
        # Run blocking IO in a thread pool so it doesn't freeze the async server
        loop = asyncio.get_event_loop()
        wav_path = await loop.run_in_executor(
            None, extract_audio, video_path, session_dir
        )
        push_progress("extract_audio", "complete", f"Audio extracted: {os.path.basename(wav_path)}")

        # ---- STEP 2: Analyse Audio ----
        push_progress("analyse_audio", "running", "Analysing tempo, energy, and spectral features...")
        audio_features = await loop.run_in_executor(
            None, analyse_audio, wav_path, session_dir
        )
        push_progress(
            "analyse_audio", "complete",
            f"Audio: {audio_features['tempo_bpm']} BPM, energy={audio_features['energy']['level_label']}"
        )

        # ---- STEP 3: Transcribe Speech ----
        push_progress("transcribe", "running", "Transcribing speech with Whisper...")
        empty_transcript = {"full_text": "", "has_speech": False, "segments": [], "words": [], "opening_words": [], "closing_words": []}
        if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                transcript = await loop.run_in_executor(
                    None, transcribe_audio, wav_path, session_dir, OPENAI_API_KEY
                )
                speech_status = f"Transcribed: {len(transcript['full_text'])} chars" if transcript['has_speech'] else "No speech detected"
            except Exception as e:
                # Transcription failed (e.g. no billing credits) — continue without it
                logger.warning(f"Transcription failed, continuing without speech data: {e}")
                transcript = empty_transcript
                speech_status = "Skipped — check OpenAI billing at platform.openai.com"
        else:
            transcript = empty_transcript
            speech_status = "Skipped (no OpenAI key)"
        push_progress("transcribe", "complete", speech_status)

        # ---- STEP 4: Extract Frames ----
        push_progress("extract_frames", "running", "Extracting key frames from video...")
        frame_files = await loop.run_in_executor(
            None, extract_frames, video_path, session_dir
        )
        push_progress("extract_frames", "complete", f"Extracted {len(frame_files)} frames")

        # Load frame metadata that was saved by extract_frames
        frame_metadata_path = os.path.join(session_dir, "frame_metadata.json")
        with open(frame_metadata_path) as f:
            frame_metadata = json.load(f)

        # ---- STEP 5: Visual Analysis (Claude Vision) ----
        # Claude looks at the extracted frames and describes what it sees.
        # No AWS needed — works for any employee with just the Anthropic key.
        push_progress("rekognition", "running", "Analysing visuals with Claude Vision...")
        if rekognition_json_path:
            # Nike test case: use the pre-loaded Rekognition JSON
            visual_analysis = load_rekognition_from_file(rekognition_json_path)
            push_progress("rekognition", "complete", "Loaded pre-existing visual data (Nike test)")
        else:
            # Standard path: analyse frames with Claude Vision
            visual_analysis = await loop.run_in_executor(
                None, analyse_frames_with_claude,
                frame_files, frame_metadata, session_dir, ANTHROPIC_API_KEY
            )
            push_progress(
                "rekognition", "complete",
                f"Visual analysis complete — {visual_analysis.get('frames_analysed', 0)} frames analysed"
            )

        # ---- STEP 6: Generate Creative Genome ----
        push_progress("genome", "running", "Generating Creative Genome with Claude AI...")
        genome = await loop.run_in_executor(
            None, generate_creative_genome,
            audio_features, transcript, visual_analysis, frame_metadata,
            brand_context, ANTHROPIC_API_KEY, session_dir
        )
        cohort = genome.get("genome", {}).get("daivid_classification", {}).get("dominant_cohort", "Unknown")
        push_progress("genome", "complete", f"Genome complete — dominant cohort: {cohort}")

        # ---- STEP 7: Score Resonance ----
        push_progress("resonance", "running", "Scoring resonance against target persona...")
        scorecard = await loop.run_in_executor(
            None, score_resonance,
            genome, brand_context, ANTHROPIC_API_KEY, session_dir
        )
        overall_score = scorecard.get("scorecard", {}).get("overall_resonance_score", "?")
        push_progress("resonance", "complete", f"Resonance score: {overall_score}/10")

        # ---- STEP 8: Generate Final Report ----
        push_progress("synthesis", "running", "Synthesising final report...")
        report = await loop.run_in_executor(
            None, generate_final_report,
            genome, scorecard, brand_context, ANTHROPIC_API_KEY, session_dir
        )
        push_progress("synthesis", "complete", "Report ready")

        # Mark session complete and store result
        active_sessions[session_id]["status"] = "complete"
        active_sessions[session_id]["result"] = {
            "session_id": session_id,
            "brand_context": brand_context,
            "genome": genome,
            "scorecard": scorecard,
            "report": report,
            "output_mode": output_mode
        }
        logger.info(f"Session {session_id}: Analysis complete")

    except Exception as e:
        logger.exception(f"Session {session_id}: Pipeline failed: {e}")
        active_sessions[session_id]["status"] = "error"
        active_sessions[session_id]["error"] = str(e)
        push_progress("error", "error", str(e))


# ---- ENTRY POINT ----

if __name__ == "__main__":
    import uvicorn
    # uvicorn is the server that runs FastAPI
    # reload=True means it automatically restarts when you save a file change
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=True,
        log_level="info"
    )
