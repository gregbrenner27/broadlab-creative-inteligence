"""
generate_pdf.py
---------------
Generates a professionally formatted PDF report from the analysis results.

Uses ReportLab, a Python library for creating PDFs programmatically.
The PDF matches Broadlab's dark design aesthetic with the white/red colour scheme.

Input:  report dictionary from synthesis_call.py
Output: a PDF file at the specified path
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ---- COLOUR PALETTE ----
# Matching Broadlab's design system
DARK_BG = colors.HexColor("#0d0d0d")
WHITE = colors.HexColor("#ffffff")
LIGHT_GREY = colors.HexColor("#a0a0a0")
RED_ACCENT = colors.HexColor("#e63946")
DARK_CARD = colors.HexColor("#1a1a1a")
MID_GREY = colors.HexColor("#333333")


def create_pdf_report(report_data: dict, output_path: str, brand_name: str = "Unknown Brand"):
    """
    Generate a PDF report from the analysis results.

    Parameters:
        report_data  - the full result dict from the analysis pipeline
        output_path  - where to save the PDF file
        brand_name   - used in the document title
    """

    logger.info(f"Generating PDF report: {output_path}")

    # Extract the relevant sections
    report = report_data.get("report", report_data)
    pdf_content = report.get("pdf_content", "")
    quick_summary = report.get("quick_summary", {})
    full_analysis = report.get("full_analysis", {})

    # Create the document with A4 page size and margins
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    # ---- DEFINE STYLES ----
    styles = getSampleStyleSheet()

    # Main title style
    title_style = ParagraphStyle(
        "BroadlabTitle",
        parent=styles["Normal"],
        fontSize=24,
        textColor=WHITE,
        fontName="Helvetica-Bold",
        spaceAfter=4*mm,
        alignment=TA_LEFT
    )

    # Section heading style
    heading_style = ParagraphStyle(
        "BroadlabHeading",
        parent=styles["Normal"],
        fontSize=14,
        textColor=RED_ACCENT,
        fontName="Helvetica-Bold",
        spaceBefore=6*mm,
        spaceAfter=3*mm
    )

    # Subheading style
    subheading_style = ParagraphStyle(
        "BroadlabSubheading",
        parent=styles["Normal"],
        fontSize=11,
        textColor=WHITE,
        fontName="Helvetica-Bold",
        spaceBefore=4*mm,
        spaceAfter=2*mm
    )

    # Body text style
    body_style = ParagraphStyle(
        "BroadlabBody",
        parent=styles["Normal"],
        fontSize=9,
        textColor=LIGHT_GREY,
        fontName="Helvetica",
        leading=14,
        spaceAfter=3*mm
    )

    # Label (small caps-style metadata label)
    label_style = ParagraphStyle(
        "BroadlabLabel",
        parent=styles["Normal"],
        fontSize=7,
        textColor=LIGHT_GREY,
        fontName="Helvetica",
        spaceAfter=1*mm
    )

    # Verdict/callout style
    verdict_style = ParagraphStyle(
        "BroadlabVerdict",
        parent=styles["Normal"],
        fontSize=12,
        textColor=WHITE,
        fontName="Helvetica-Bold",
        leading=18,
        spaceAfter=4*mm
    )

    # ---- BUILD CONTENT ----
    story = []

    # ---- COVER / HEADER ----
    story.append(Paragraph("BROADLAB", ParagraphStyle(
        "Cover", parent=styles["Normal"], fontSize=9, textColor=RED_ACCENT,
        fontName="Helvetica-Bold", spaceAfter=2*mm
    )))
    story.append(Paragraph("Creative Intelligence Report", title_style))
    story.append(Paragraph(brand_name, ParagraphStyle(
        "BrandName", parent=styles["Normal"], fontSize=16, textColor=WHITE,
        fontName="Helvetica", spaceAfter=2*mm
    )))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%d %B %Y')}",
        label_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=RED_ACCENT, spaceAfter=6*mm))

    # ---- EXECUTIVE SUMMARY BOX ----
    if quick_summary:
        story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))

        verdict = quick_summary.get("verdict", "")
        if verdict:
            story.append(Paragraph(f'"{verdict}"', verdict_style))

        # Score box using a table
        overall_score = quick_summary.get("overall_score", "–")
        top_audience = quick_summary.get("top_recommended_audience", "–")
        score_data = [
            [
                Paragraph("OVERALL RESONANCE SCORE", label_style),
                Paragraph("PRIMARY RECOMMENDED AUDIENCE", label_style)
            ],
            [
                Paragraph(f"<font size='28' color='#e63946'><b>{overall_score}</b></font><font size='12' color='#a0a0a0'>/10</font>", body_style),
                Paragraph(f"<font color='#ffffff'>{top_audience}</font>", body_style)
            ]
        ]
        score_table = Table(score_data, colWidths=[85*mm, 85*mm])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), DARK_CARD),
            ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 4*mm))

        # Strengths and gaps in a two-column table
        strengths = quick_summary.get("three_strengths", [])
        gaps = quick_summary.get("two_critical_gaps", [])

        sg_data = [
            [Paragraph("KEY STRENGTHS", label_style), Paragraph("CRITICAL GAPS", label_style)],
        ]
        max_rows = max(len(strengths), len(gaps))
        for i in range(max_rows):
            s_text = f"<font color='#ffffff'>+ {strengths[i]}</font>" if i < len(strengths) else ""
            g_text = f"<font color='#e63946'>! {gaps[i]}</font>" if i < len(gaps) else ""
            sg_data.append([
                Paragraph(s_text, body_style),
                Paragraph(g_text, body_style)
            ])

        sg_table = Table(sg_data, colWidths=[85*mm, 85*mm])
        sg_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), DARK_CARD),
            ("BACKGROUND", (0, 0), (-1, 0), MID_GREY),
            ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(sg_table)
        story.append(Spacer(1, 4*mm))

        # Targeting recommendation
        targeting = quick_summary.get("targeting_recommendation", "")
        if targeting:
            story.append(Paragraph("TARGETING RECOMMENDATION", heading_style))
            story.append(Paragraph(targeting, body_style))

    # ---- PAGE BREAK BEFORE FULL ANALYSIS ----
    story.append(PageBreak())

    # ---- FULL ANALYSIS ----
    if pdf_content:
        # The pdf_content from Claude is already formatted prose
        # Split it by double newlines to create paragraphs
        story.append(Paragraph("FULL ANALYSIS", heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY, spaceAfter=4*mm))

        paragraphs = pdf_content.split("\n\n")
        for para_text in paragraphs:
            para_text = para_text.strip()
            if not para_text:
                continue

            # Detect section headers (lines in all caps or starting with a known keyword)
            if para_text.isupper() or para_text.startswith("#"):
                clean = para_text.replace("#", "").strip()
                story.append(Paragraph(clean, subheading_style))
            else:
                story.append(Paragraph(para_text, body_style))

    elif full_analysis:
        # Fallback: use structured full_analysis data
        story.append(Paragraph("FULL ANALYSIS", heading_style))

        if full_analysis.get("overall_verdict"):
            story.append(Paragraph("Overall Verdict", subheading_style))
            story.append(Paragraph(full_analysis["overall_verdict"], body_style))

        if full_analysis.get("creative_genome_narrative"):
            story.append(Paragraph("Creative Genome", subheading_style))
            story.append(Paragraph(full_analysis["creative_genome_narrative"], body_style))

        # Persona scorecards
        for persona in full_analysis.get("persona_scorecards", []):
            story.append(Paragraph(
                f"Persona: {persona.get('persona_name', 'Unknown')}",
                subheading_style
            ))

            # Score table
            scores = persona.get("dimension_scores", {})
            score_rows = [
                [Paragraph("Dimension", label_style), Paragraph("Score", label_style)],
                ["Emotional Power", str(scores.get("emotional_power", "–"))],
                ["Emotional Register Match", str(scores.get("emotional_register_match", "–"))],
                ["Identity Signal Fit", str(scores.get("identity_signal_fit", "–"))],
                ["Motivational Alignment", str(scores.get("motivational_alignment", "–"))],
                ["Attention Architecture Fit", str(scores.get("attention_architecture_fit", "–"))],
                [
                    Paragraph("<b>Overall Resonance Score</b>", body_style),
                    Paragraph(f"<b><font color='#e63946'>{persona.get('overall_score', '–')}</font>/10</b>", body_style)
                ]
            ]

            score_table = Table(score_rows, colWidths=[120*mm, 50*mm])
            score_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), MID_GREY),
                ("BACKGROUND", (0, -1), (-1, -1), DARK_CARD),
                ("BACKGROUND", (0, 1), (-1, -2), DARK_CARD),
                ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("TEXTCOLOR", (0, 1), (0, -1), LIGHT_GREY),
                ("TEXTCOLOR", (1, 1), (1, -2), WHITE),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
            ]))
            story.append(score_table)
            story.append(Spacer(1, 3*mm))

            budget = persona.get("budget_concentration", "–")
            story.append(Paragraph(
                f"Budget Concentration: <b><font color='#e63946'>{budget}</font></b>",
                body_style
            ))

    # ---- FOOTER NOTE ----
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MID_GREY, spaceAfter=3*mm))
    story.append(Paragraph(
        "This report was generated by the Broadlab Creative Intelligence Platform. "
        "Scores are AI-generated based on Emotional Power, Emotional Register Match, "
        "Identity Signal Fit, Motivational Alignment, and Attention Architecture Fit. "
        "DAIVID emotion scores and Snowflake postcode data will enhance accuracy when available.",
        label_style
    ))

    # ---- CANVAS BACKGROUND ----
    def on_page(canvas, doc):
        """Draw dark background on every page."""
        canvas.saveState()
        canvas.setFillColor(DARK_BG)
        canvas.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
        canvas.restoreState()

    # Build the PDF
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    logger.info(f"PDF generated: {output_path}")
