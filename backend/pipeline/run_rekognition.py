"""
run_rekognition.py
------------------
Pipeline Step 5: Run AWS Rekognition video analysis on the uploaded ad.

AWS Rekognition is Amazon's AI vision service. We use it to detect:
- Labels: objects, settings, and activities in the video ("running", "stadium", "crowd")
- Faces: facial expressions and demographics
- Celebrities: recognisable public figures (athletes, actors, musicians)
- Moderation: anything flagged as sensitive content

IMPORTANT: Rekognition video analysis is asynchronous — meaning we send the
video, get back a job ID, then poll (check repeatedly) until the analysis is
done. This process typically takes 1–3 minutes for a 30-second ad.

The video must be uploaded to an S3 bucket first before Rekognition can
process it. S3 is Amazon's file storage service.

Input:  path to the MP4 file
Output: rekognition.json containing all detected labels, faces, and celebrities
"""

import boto3        # AWS Python library
import json
import os
import time
import logging

logger = logging.getLogger(__name__)


def run_rekognition_analysis(
    mp4_path: str,
    temp_dir: str,
    aws_access_key: str,
    aws_secret_key: str,
    aws_region: str,
    s3_bucket: str,
    rekognition_role_arn: str
) -> dict:
    """
    Upload video to S3 and run AWS Rekognition analysis.

    Parameters:
        mp4_path            - full file path to the input MP4 video
        temp_dir            - folder where rekognition.json will be saved
        aws_access_key      - from .env: AWS_ACCESS_KEY_ID
        aws_secret_key      - from .env: AWS_SECRET_ACCESS_KEY
        aws_region          - from .env: AWS_REGION (e.g. eu-west-2)
        s3_bucket           - from .env: AWS_S3_BUCKET (name of your S3 bucket)
        rekognition_role_arn - from .env: AWS_REKOGNITION_ROLE_ARN

    Returns:
        Dictionary containing all Rekognition results
    """

    # Create AWS client sessions
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    s3_client = session.client("s3")
    rekognition_client = session.client("rekognition")

    # Upload the video to S3 — Rekognition reads from S3, not local files
    video_filename = os.path.basename(mp4_path)
    s3_key = f"broadlab-analysis/{video_filename}"

    logger.info(f"Uploading video to S3: s3://{s3_bucket}/{s3_key}")
    with open(mp4_path, "rb") as video_file:
        s3_client.upload_fileobj(video_file, s3_bucket, s3_key)
    logger.info("S3 upload complete")

    # Reference to the S3 video for Rekognition
    s3_video = {"S3Object": {"Bucket": s3_bucket, "Name": s3_key}}

    # --- START ALL FOUR REKOGNITION JOBS ---
    # Each job analyses a different aspect of the video
    logger.info("Starting Rekognition analysis jobs...")

    # Job 1: Label detection — what objects, settings, activities are in the video
    label_job = rekognition_client.start_label_detection(
        Video=s3_video,
        MinConfidence=70  # only return labels Rekognition is 70%+ confident about
    )

    # Job 2: Face detection — find faces and read expressions
    face_job = rekognition_client.start_face_detection(
        Video=s3_video,
        FaceAttributes="ALL"  # get all available face attributes including emotion
    )

    # Job 3: Celebrity recognition — identify known public figures
    celebrity_job = rekognition_client.start_celebrity_recognition(
        Video=s3_video
    )

    # Job 4: Content moderation — flag any sensitive content
    moderation_job = rekognition_client.start_content_moderation(
        Video=s3_video,
        MinConfidence=70
    )

    job_ids = {
        "labels": label_job["JobId"],
        "faces": face_job["JobId"],
        "celebrities": celebrity_job["JobId"],
        "moderation": moderation_job["JobId"]
    }
    logger.info(f"Rekognition jobs started: {job_ids}")

    # --- POLL FOR COMPLETION ---
    # We check every 10 seconds until all four jobs are done
    # Maximum wait: 10 minutes (600 seconds)
    results = {}
    max_wait_seconds = 600
    poll_interval = 10

    for job_type, job_id in job_ids.items():
        logger.info(f"Waiting for {job_type} job {job_id} to complete...")
        elapsed = 0

        while elapsed < max_wait_seconds:
            # Check job status based on job type
            if job_type == "labels":
                response = rekognition_client.get_label_detection(JobId=job_id)
            elif job_type == "faces":
                response = rekognition_client.get_face_detection(JobId=job_id)
            elif job_type == "celebrities":
                response = rekognition_client.get_celebrity_recognition(JobId=job_id)
            elif job_type == "moderation":
                response = rekognition_client.get_content_moderation(JobId=job_id)

            status = response["JobStatus"]
            if status == "SUCCEEDED":
                logger.info(f"{job_type} job complete")
                results[job_type] = response
                break
            elif status == "FAILED":
                logger.error(f"{job_type} job failed: {response.get('StatusMessage')}")
                results[job_type] = {"error": response.get("StatusMessage", "Unknown failure")}
                break
            else:
                # Still IN_PROGRESS — wait and try again
                time.sleep(poll_interval)
                elapsed += poll_interval

        if elapsed >= max_wait_seconds:
            logger.error(f"{job_type} job timed out after {max_wait_seconds}s")
            results[job_type] = {"error": "Timed out waiting for Rekognition job"}

    # --- PROCESS AND SUMMARISE RESULTS ---
    processed = _process_rekognition_results(results)

    # Save the full results to JSON
    output_path = os.path.join(temp_dir, "rekognition.json")
    with open(output_path, "w") as f:
        json.dump(processed, f, indent=2)

    # Clean up — delete the video from S3 to avoid storage costs
    try:
        s3_client.delete_object(Bucket=s3_bucket, Key=s3_key)
        logger.info("Cleaned up S3 upload")
    except Exception as e:
        logger.warning(f"Failed to clean up S3 object: {e}")

    logger.info("Rekognition analysis complete")
    return processed


def _process_rekognition_results(raw_results: dict) -> dict:
    """
    Clean and summarise the raw Rekognition API responses into a useful structure.
    This removes pagination and redundant data, keeping only what Claude needs.
    """

    processed = {}

    # Process label detections — group by label name, keep top 20 by confidence
    if "labels" in raw_results and "Labels" in raw_results["labels"]:
        label_counts = {}
        for item in raw_results["labels"]["Labels"]:
            label = item["Label"]
            name = label["Name"]
            confidence = label["Confidence"]
            if name not in label_counts or label_counts[name]["max_confidence"] < confidence:
                label_counts[name] = {
                    "name": name,
                    "max_confidence": round(confidence, 1),
                    "categories": [c["Name"] for c in label.get("Categories", [])]
                }

        # Sort by confidence and take top 30
        top_labels = sorted(
            label_counts.values(),
            key=lambda x: x["max_confidence"],
            reverse=True
        )[:30]
        processed["labels"] = top_labels

    # Process celebrity detections — deduplicate by name
    if "celebrities" in raw_results and "Celebrities" in raw_results["celebrities"]:
        celebrity_dict = {}
        for item in raw_results["celebrities"]["Celebrities"]:
            celeb = item["Celebrity"]
            name = celeb["Name"]
            confidence = celeb["Confidence"]
            if name not in celebrity_dict or celebrity_dict[name]["confidence"] < confidence:
                celebrity_dict[name] = {
                    "name": name,
                    "confidence": round(confidence, 1),
                    "urls": celeb.get("Urls", [])
                }
        processed["celebrities"] = list(celebrity_dict.values())
        processed["has_celebrities"] = len(celebrity_dict) > 0

    # Process face detections — summarise emotions across all detected faces
    if "faces" in raw_results and "Faces" in raw_results["faces"]:
        emotions_totals = {}
        face_count = 0
        for item in raw_results["faces"]["Faces"]:
            face = item["Face"]
            face_count += 1
            for emotion in face.get("Emotions", []):
                emo_type = emotion["Type"]
                emo_confidence = emotion["Confidence"]
                if emo_type not in emotions_totals:
                    emotions_totals[emo_type] = 0
                emotions_totals[emo_type] += emo_confidence

        # Average emotion scores across all face detections
        avg_emotions = {
            k: round(v / face_count, 1)
            for k, v in emotions_totals.items()
        } if face_count > 0 else {}

        processed["faces"] = {
            "total_detections": face_count,
            "dominant_emotions": dict(
                sorted(avg_emotions.items(), key=lambda x: x[1], reverse=True)[:5]
            )
        }

    # Process moderation labels — flag anything detected
    if "moderation" in raw_results and "ModerationLabels" in raw_results["moderation"]:
        mod_labels = [
            {
                "name": item["ModerationLabel"]["Name"],
                "confidence": round(item["ModerationLabel"]["Confidence"], 1)
            }
            for item in raw_results["moderation"]["ModerationLabels"]
        ]
        processed["moderation_flags"] = mod_labels
        processed["has_moderation_flags"] = len(mod_labels) > 0

    return processed


def load_rekognition_from_file(json_path: str) -> dict:
    """
    Load pre-existing Rekognition results from a JSON file and convert to
    the processed format the pipeline expects. Handles the raw flat export
    format (Labels/Celebrities/ModerationLabels at top level with Timestamps).
    """
    with open(json_path, "r") as f:
        raw = json.load(f)

    processed = {}

    # --- LABELS ---
    # Raw format: [{"Timestamp": 0, "Label": {"Name": "...", "Confidence": 91.7, ...}}]
    if "Labels" in raw:
        label_counts = {}
        for item in raw["Labels"]:
            label = item.get("Label", {})
            name = label.get("Name", "")
            confidence = label.get("Confidence", 0)
            categories = [c["Name"] for c in label.get("Categories", [])]
            if name not in label_counts or label_counts[name]["max_confidence"] < confidence:
                label_counts[name] = {
                    "name": name,
                    "max_confidence": round(confidence, 1),
                    "categories": categories
                }
        processed["labels"] = sorted(
            label_counts.values(), key=lambda x: x["max_confidence"], reverse=True
        )[:30]

    # --- CELEBRITIES ---
    # Raw format: [{"Timestamp": 1501, "Celebrity": {"Name": "...", "Confidence": 89.1, ...}}]
    if "Celebrities" in raw:
        celeb_dict = {}
        for item in raw["Celebrities"]:
            celeb = item.get("Celebrity", {})
            name = celeb.get("Name", "")
            confidence = celeb.get("Confidence", 0)
            if name not in celeb_dict or celeb_dict[name]["confidence"] < confidence:
                celeb_dict[name] = {
                    "name": name,
                    "confidence": round(confidence, 1),
                    "urls": celeb.get("Urls", [])
                }
        processed["celebrities"] = list(celeb_dict.values())
        processed["has_celebrities"] = len(celeb_dict) > 0

    # --- MODERATION ---
    if "ModerationLabels" in raw:
        mod_labels = [
            {
                "name": item["ModerationLabel"]["Name"],
                "confidence": round(item["ModerationLabel"]["Confidence"], 1)
            }
            for item in raw["ModerationLabels"]
            if "ModerationLabel" in item
        ]
        processed["moderation_flags"] = mod_labels
        processed["has_moderation_flags"] = len(mod_labels) > 0

    # No Faces key in this export format
    processed["faces"] = {"total_detections": 0, "dominant_emotions": {}}

    return processed
