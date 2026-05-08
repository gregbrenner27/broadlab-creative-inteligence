"""
analyse_audio.py
----------------
Pipeline Step 2: Analyse the audio track using Librosa.

Librosa is a Python library for music and audio analysis. It reads the WAV
file and extracts numerical features that describe the sound: how fast it is
(tempo), how loud it is (energy), and what kind of tonal quality it has
(spectral centroid — think of this as brightness vs darkness of sound).

These features are passed to Claude in Step 6 to help it classify the
emotional register of the ad's music.

Input:  path to the WAV file from Step 1
Output: dictionary of audio features, saved as audio_features.json
"""

import librosa          # audio analysis library
import librosa.beat     # beat detection module within librosa
import numpy as np      # numerical computing library
import json
import os
import logging

logger = logging.getLogger(__name__)


def analyse_audio(wav_path: str, temp_dir: str) -> dict:
    """
    Analyse audio features from a WAV file using Librosa.

    Parameters:
        wav_path  - full file path to the input WAV file
        temp_dir  - folder where audio_features.json will be saved

    Returns:
        Dictionary containing all audio features
    """

    logger.info(f"Analysing audio: {wav_path}")

    # Load the audio file into Librosa
    # y = the audio signal as a numpy array (just a list of numbers representing sound waves)
    # sr = sample rate (how many audio samples per second — we get 44100)
    y, sr = librosa.load(wav_path, sr=None)

    duration_seconds = float(len(y) / sr)
    logger.info(f"Audio duration: {duration_seconds:.1f} seconds")

    # --- TEMPO AND BEAT ANALYSIS ---
    # BPM = beats per minute. Higher BPM = faster music.
    # 60-80 BPM = slow (ballad territory)
    # 80-120 BPM = medium (pop, commercial)
    # 120-160 BPM = fast (dance, hip-hop)
    # 160+ BPM = very fast (drum & bass, intense energy)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    tempo_bpm = float(tempo) if np.isscalar(tempo) else float(tempo[0])

    # Convert beat frame positions to timestamps in seconds
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

    # --- ENERGY ANALYSIS (RMS) ---
    # RMS = Root Mean Square — essentially the average loudness across the audio
    # We measure it in short windows and average across the whole track
    # Values range from ~0.0 (near silence) to ~1.0 (maximum loudness)
    rms = librosa.feature.rms(y=y)
    rms_mean = float(np.mean(rms))
    rms_max = float(np.max(rms))
    rms_min = float(np.min(rms))

    # Map RMS mean to a human-readable energy level
    if rms_mean < 0.05:
        energy_level = "very low"
    elif rms_mean < 0.1:
        energy_level = "low"
    elif rms_mean < 0.2:
        energy_level = "medium"
    elif rms_mean < 0.35:
        energy_level = "high"
    else:
        energy_level = "very high"

    # --- SPECTRAL CENTROID ---
    # The spectral centroid is the "centre of gravity" of the sound spectrum
    # High values = bright, sharp, clear sound (electronic, synth-heavy)
    # Low values = dark, warm, bass-heavy sound (acoustic, orchestral, soul)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = float(np.mean(spectral_centroid))

    if spectral_centroid_mean < 1500:
        spectral_character = "dark and warm"
    elif spectral_centroid_mean < 2500:
        spectral_character = "balanced"
    elif spectral_centroid_mean < 4000:
        spectral_character = "bright and clear"
    else:
        spectral_character = "very bright and sharp"

    # --- ZERO CROSSING RATE ---
    # How often the audio signal crosses zero — high values indicate noise/percussion,
    # low values indicate sustained tones. Helps distinguish speech from music.
    zcr = librosa.feature.zero_crossing_rate(y=y)
    zcr_mean = float(np.mean(zcr))

    # --- MFCC (Mel-Frequency Cepstral Coefficients) ---
    # These 13 numbers summarise the tonal character of the audio.
    # Used by Claude to understand the "texture" of the sound.
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_means = np.mean(mfcc, axis=1).tolist()

    # --- ASSEMBLE THE FEATURES DICTIONARY ---
    audio_features = {
        "duration_seconds": round(duration_seconds, 1),
        "tempo_bpm": round(tempo_bpm, 1),
        "beat_times_seconds": [round(t, 2) for t in beat_times[:20]],  # first 20 beats
        "energy": {
            "rms_mean": round(rms_mean, 4),
            "rms_max": round(rms_max, 4),
            "rms_min": round(rms_min, 4),
            "level_label": energy_level
        },
        "spectral": {
            "centroid_mean_hz": round(spectral_centroid_mean, 1),
            "character_label": spectral_character,
            "zero_crossing_rate_mean": round(zcr_mean, 4)
        },
        "mfcc_signature": [round(v, 2) for v in mfcc_means]
    }

    # Save to JSON file in the temp directory
    output_path = os.path.join(temp_dir, "audio_features.json")
    with open(output_path, "w") as f:
        json.dump(audio_features, f, indent=2)

    logger.info(
        f"Audio analysis complete: {tempo_bpm:.0f} BPM, "
        f"energy={energy_level}, spectral={spectral_character}"
    )
    return audio_features
