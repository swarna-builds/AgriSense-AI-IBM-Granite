import os
from typing import Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. Register system Arial font binaries
try:
    font_path = "C:/Windows/Fonts/arial.ttf"
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"
    if os.path.exists(font_path) and os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont("Arial", font_path))
        pdfmetrics.registerFont(TTFont("Arial-Bold", font_bold_path))
        MAIN_FONT, BOLD_FONT = "Arial", "Arial-Bold"
    else:
        MAIN_FONT, BOLD_FONT = "Helvetica", "Helvetica-Bold"
except Exception:
    MAIN_FONT, BOLD_FONT = "Helvetica", "Helvetica-Bold"

def add_footer(canvas_obj: Any, doc: Any) -> None:
    """Draws standard footer with page numbers using public ReportLab API."""
    canvas_obj.saveState()
    canvas_obj.setFont(MAIN_FONT, 10)
    canvas_obj.setFillColor(colors.HexColor("#718096"))
    canvas_obj.drawString(54, 30, "AgriSense AI — Problem Statement & Objectives | IBM watsonx.ai")
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawRightString(612 - 54, 30, f"Page {page_num}")
    canvas_obj.restoreState()

def generate_pdf(output_filename="yourproblemstatement.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Template Specifications: Font Arial | Heading 28pt | Content 20pt
    heading_style = ParagraphStyle(
        "TemplateHeading",
        parent=styles["Normal"],
        fontName=BOLD_FONT,
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#0f3b2e"),
        spaceBefore=14,
        spaceAfter=12
    )

    content_style = ParagraphStyle(
        "TemplateContent",
        parent=styles["Normal"],
        fontName=MAIN_FONT,
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=14
    )

    bullet_style = ParagraphStyle(
        "TemplateBullet",
        parent=styles["Normal"],
        fontName=MAIN_FONT,
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#2d3748"),
        leftIndent=24,
        spaceAfter=10
    )

    meta_style = ParagraphStyle(
        "TemplateMeta",
        parent=styles["Normal"],
        fontName=MAIN_FONT,
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#4a5568"),
        spaceAfter=14
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("Problem Statement: AgriSense AI", heading_style))
    story.append(Paragraph("<b>Domain:</b> Agriculture &nbsp;|&nbsp; <b>Model:</b> IBM Granite (ibm/granite-4-h-small)", meta_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0f3b2e"), spaceAfter=18))

    # The Challenge Section
    story.append(Paragraph("The Challenge", heading_style))
    story.append(Paragraph(
        "Smallholder agriculture remains acutely vulnerable to rapid weather shifts, sudden pathogen outbreaks, and uncalibrated chemical use:",
        content_style
    ))
    story.append(Paragraph("• <b>Epiphytotic Vulnerability:</b> Fungal pathogens like Late Blight and Anthracnose cause severe crop loss when humidity and rain cross biological thresholds before manual detection.", bullet_style))
    story.append(Paragraph("• <b>Agrochemical Overdosing:</b> Cultivators apply excessive broad-spectrum chemicals without diagnostic guidance, causing phytotoxicity and soil degradation.", bullet_style))
    story.append(Paragraph("• <b>LLM Hallucination Hazards:</b> General-purpose AI tools regularly recommend inaccurate dosages and dangerous tank mixtures not grounded in verified packages of practices.", bullet_style))
    story.append(Paragraph("• <b>Vernacular Language Barriers:</b> Critical agrometeorological advisories rarely reach farmers in regional native dialects.", bullet_style))

    story.append(Spacer(1, 14))

    # The Objective Section
    story.append(Paragraph("The Objective", heading_style))
    story.append(Paragraph(
        "Build AgriSense AI, an autonomous agronomic decision platform powered by IBM watsonx.ai and IBM Granite:",
        content_style
    ))
    story.append(Paragraph("• <b>Autonomous Sentinel Daemon:</b> Continuously monitor hyper-local weather telemetry (temperature, humidity, rain probability) to issue zero-latency risk alerts.", bullet_style))
    story.append(Paragraph("• <b>Multi-Modal Pathology Vision:</b> Segment foliar lesions and fruit rot craters from field photos to classify plant infections.", bullet_style))
    story.append(Paragraph("• <b>ICAR-Grounded RAG Retrieval:</b> Fetch verified active ingredients and exact per-liter dilution formulas from agronomic research datasets.", bullet_style))
    story.append(Paragraph("• <b>Granite Decision Fusion:</b> Deploy Granite-4-H-Small to generate actionable 7-day field schedules and simulated chemical trade-offs in structured JSON.", bullet_style))
    story.append(Paragraph("• <b>Vernacular Voice Delivery:</b> Deliver complete operational decisions in Kannada, Telugu, Hindi, and English with audio speech synthesis.", bullet_style))

    story.append(Spacer(1, 14))

    # Expected Outcomes Section
    story.append(Paragraph("Projected Field Outcomes", heading_style))
    story.append(Paragraph("• <b>Yield Loss Prevention:</b> Preempt active fungal sporulation with a 48-to-72 hour lead time.", bullet_style))
    story.append(Paragraph("• <b>Input Cost Optimization:</b> Reduce excess chemical use by timing spraying strictly to weather-pathology infection windows.", bullet_style))
    story.append(Paragraph("• <b>Zero-Hallucination Safety:</b> Ground every curative spray recommendation strictly in vetted ICAR university protocols.", bullet_style))

    # Build document using official callbacks
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    # Save identical duplicate copy so both filename variations exist
    with open(output_filename, "rb") as src, open("problemstatement.pdf", "wb") as dst:
        dst.write(src.read())

    print("Generated both 'yourproblemstatement.pdf' and 'problemstatement.pdf' successfully.")

if __name__ == "__main__":
    generate_pdf()