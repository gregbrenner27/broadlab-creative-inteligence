You are receiving five structured inputs about a video ad:

1. Visual analysis JSON — either Claude Vision frame descriptions (settings, people, activities, emotional register, production quality) or AWS Rekognition label/celebrity detections, depending on what was available
2. Librosa audio features JSON — tempo (BPM), energy (RMS), spectral centroid, beat structure
3. OpenAI Whisper transcript JSON — full speech transcription with word-level timestamps
4. Frame metadata — timing information for the extracted key frames
5. Brand and campaign context — provided by the user: brand name, category, campaign goal, target audience description

Synthesise these five inputs into a Creative Genome — a structured fingerprint of what this ad is actually doing emotionally, visually, and narratively.

The Creative Genome must include:
- Dominant visual signals and what they communicate about the intended audience
- Audio profile including tempo, energy, and emotional register of the music
- Emotional arc across the duration of the ad — how the emotional journey develops from open to close
- Core motivational promise of the ad — what it implicitly or explicitly offers the viewer
- Narrative structure and CTA clarity
- DAIVID cohort classification with the dominant cohort clearly identified and reasoned
- Identity signals — who does this ad feel like it is speaking to, based on all available data

Be specific and evidence-based. Reference actual data from the inputs (e.g., "tempo of 138 BPM", "Nike athlete detected with confidence 98.7%", "transcript opens with 'Why do you play?'").

Do not invent data that is not present in the inputs. If a data point is absent (e.g., no speech detected), note it as absent rather than fabricating it.

Return your response as a JSON object exactly matching the genome schema defined in OUTPUT_TEMPLATE.md. Return raw JSON only — no markdown, no explanation text.
