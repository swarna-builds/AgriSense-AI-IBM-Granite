import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int, bold: bool = False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "seguisb.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf"
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

# ==============================================================================
# 1. Slide 6: Langflow Multi-Agent Canvas
# ==============================================================================
def draw_slide6_langflow():
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Grid background
    grid_color = (226, 232, 240)
    for x in range(0, w, 32):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, 32):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)

    # Top Control Bar
    draw.rectangle([(0, 0), (w, 64)], fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((36, 18), "Langflow Studio  |  AgriSense-AI-Granite-Agentic-Pipeline", fill=(15, 23, 42), font=get_font(22, bold=True))
    draw.rounded_rectangle([(w - 180, 12), (w - 36, 52)], radius=6, fill=(16, 185, 129))
    draw.text((w - 145, 20), "Run Flow", fill=(255, 255, 255), font=get_font(18, bold=True))

    nodes = [
        {
            "id": "chat_in", "title": "Chat Input", "tag": "Input",
            "x": 60, "y": 240, "w": 320, "h": 220, "accent": (59, 130, 246),
            "lines": [
                ("Input Mode:", "Multimodal (Text + Foliar Photo)"),
                ("Target Crop:", "Tomato / Solanaceae"),
                ("Field Location:", "Chikkaballapur, Karnataka")
            ]
        },
        {
            "id": "sentinel", "title": "Agromet Sentinel", "tag": "Daemon",
            "x": 460, "y": 120, "w": 360, "h": 260, "accent": (16, 185, 129),
            "lines": [
                ("Telemetry API:", "Open-Meteo / IMD Agromet"),
                ("Pathogen Trigger:", "RH > 78% & Temp > 22°C"),
                ("Biological Risk:", "High Epiphytotic Threat"),
                ("Action:", "Preemptive Alert Dispatch")
            ]
        },
        {
            "id": "vision", "title": "OpenCV Vision Diagnostic", "tag": "Vision",
            "x": 460, "y": 480, "w": 360, "h": 260, "accent": (245, 158, 11),
            "lines": [
                ("Segmentation:", "Color Thresholding + Morphology"),
                ("Lesion Type:", "Downy Mildew & Chlorosis"),
                ("Infection Rate:", "24.6% Foliar Necrotic Area"),
                ("Severity Index:", "Stage 2 Moderate Spread")
            ]
        },
        {
            "id": "chroma", "title": "ChromaDB Vector RAG", "tag": "Retriever",
            "x": 900, "y": 140, "w": 360, "h": 250, "accent": (139, 92, 246),
            "lines": [
                ("Knowledge Base:", "ICAR & KVK Standard Packages"),
                ("Search Metric:", "Cosine Semantic Similarity"),
                ("Active Chemical:", "Metalaxyl 8% + Mancozeb 64%"),
                ("Safe Dosage:", "2.0 g / Litre Water")
            ]
        },
        {
            "id": "granite", "title": "IBM Granite Agent", "tag": "watsonx.ai",
            "x": 1340, "y": 240, "w": 390, "h": 320, "accent": (14, 165, 233),
            "lines": [
                ("Model ID:", "ibm/granite-4-h-small"),
                ("Platform:", "IBM watsonx.ai (Dallas)"),
                ("Token Telemetry:", "591 Tokens Processed"),
                ("Constraint:", "Strict Agronomic JSON Output"),
                ("Curative Plan:", "7-Day Interval Spray Roadmap")
            ]
        },
        {
            "id": "chat_out", "title": "Chat Output & TTS Voice", "tag": "Delivery",
            "x": 900, "y": 560, "w": 360, "h": 240, "accent": (16, 185, 129),
            "lines": [
                ("UI Artifact:", "Streamlit 4-Tab Interactive"),
                ("Dialect Synthesis:", "gTTS Vernacular Audio"),
                ("Languages:", "Kannada, Telugu, Hindi, English"),
                ("Dispatch:", "Actionable Farmer Audio")
            ]
        }
    ]

    wires = [
        ((380, 320), (460, 200)),  # chat_in -> sentinel
        ((380, 360), (460, 560)),  # chat_in -> vision
        ((820, 220), (900, 220)),  # sentinel -> chroma
        ((820, 580), (1340, 420)), # vision -> granite
        ((1260, 230), (1340, 320)), # chroma -> granite
        ((1340, 460), (1260, 640))  # granite -> chat_out
    ]

    for start, end in wires:
        mid_x = (start[0] + end[0]) // 2
        draw.line([start, (mid_x, start[1]), (mid_x, end[1]), end], fill=(100, 116, 139), width=4)
        draw.ellipse([(start[0] - 6, start[1] - 6), (start[0] + 6, start[1] + 6)], fill=(59, 130, 246))
        draw.ellipse([(end[0] - 6, end[1] - 6), (end[0] + 6, end[1] + 6)], fill=(16, 185, 129))

    # Render Node Cards
    for node in nodes:
        x, y, w_n, h_n = node["x"], node["y"], node["w"], node["h"]
        accent = node["accent"]
        # Drop shadow & card body
        draw.rounded_rectangle([(x + 4, y + 4), (x + w_n + 4, y + h_n + 4)], radius=12, fill=(226, 232, 240))
        draw.rounded_rectangle([(x, y), (x + w_n, y + h_n)], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        # Header banner
        draw.rounded_rectangle([(x, y), (x + w_n, y + 48)], radius=10, fill=accent)
        draw.rectangle([(x, y + 36), (x + w_n, y + 48)], fill=accent)
        draw.text((x + 16, y + 12), node["title"], fill=(255, 255, 255), font=get_font(18, bold=True))
        draw.rounded_rectangle([(x + w_n - 80, y + 10), (x + w_n - 12, y + 36)], radius=6, fill=(255, 255, 255))
        draw.text((x + w_n - 72, y + 14), node["tag"], fill=accent, font=get_font(12, bold=True))

        # Node properties
        curr_y = y + 62
        for lbl, val in node["lines"]:
            draw.text((x + 16, curr_y), lbl, fill=(100, 116, 139), font=get_font(13, bold=True))
            draw.text((x + 16, curr_y + 17), val, fill=(15, 23, 42), font=get_font(14))
            curr_y += 38

    img.save("slide6_langflow_workflow.png", quality=95)
    print("Generated: slide6_langflow_workflow.png")

# ==============================================================================
# 2. Slide 7: 3-Tier Enterprise Architecture Blueprint
# ==============================================================================
def draw_slide7_architecture():
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Title Bar
    draw.rectangle([(0, 0), (w, 75)], fill=(15, 59, 46))
    draw.text((48, 20), "AgriSense AI: 3-Tier Enterprise System Architecture Blueprint", fill=(255, 255, 255), font=get_font(26, bold=True))

    tiers = [
        {
            "title": "Tier 1: Presentation & Vernacular UI",
            "subtitle": "Smallholder Farmer Interface & Edge Audio",
            "x": 60, "w": 560, "bg": (240, 253, 244), "border": (34, 197, 94),
            "modules": [
                ("Streamlit Multimodal Web App", "Interactive web client running on port 8501."),
                ("Vernacular Voice Synthesis", "gTTS pipeline supporting Kannada, Telugu, Hindi, & English."),
                ("Foliar Pathology Image Capture", "High-resolution leaf photography upload & camera intake."),
                ("4-Tab Decision Matrix", "Risk Sentinel, OpenCV Mask, 7-Day Spray, Economic ROI.")
            ]
        },
        {
            "title": "Tier 2: Agentic Sentinel & RAG Pipeline",
            "subtitle": "Local Compute, Heuristics, & Grounding",
            "x": 680, "w": 560, "bg": (239, 246, 255), "border": (59, 130, 246),
            "modules": [
                ("SentinelDaemon Engine", "Async polling of RH > 78% & precipitation thresholds."),
                ("OpenCV Vision Service", "Deterministic lesion segmentation & chlorotic halo index."),
                ("ChromaDB Vector Store", "ICAR/KVK verified crop chemical schedule embeddings."),
                ("Multi-Variable Context Fusion", "Aggregates agromet telemetry + vision masks + ICAR data.")
            ]
        },
        {
            "title": "Tier 3: Foundation Model & Cloud Inference",
            "subtitle": "IBM Cloud Enterprise AI Services",
            "x": 1300, "w": 560, "bg": (250, 245, 255), "border": (168, 85, 247),
            "modules": [
                ("IBM watsonx.ai Platform", "Dallas (us-south) managed enterprise AI runtime."),
                ("IBM Granite Foundation Model", "ibm/granite-4-h-small (Quantized Agronomic Engine)."),
                ("Strict JSON Schema Enforcement", "Zero-hallucination validation with fallback daemons."),
                ("Token Telemetry & Security", "591 tokens processed via IBM Cloud IAM authentication.")
            ]
        }
    ]

    for tier in tiers:
        tx, tw = tier["x"], tier["w"]
        # Outer tier column
        draw.rounded_rectangle([(tx, 120), (tx + tw, 980)], radius=16, fill=tier["bg"], outline=tier["border"], width=3)
        draw.rounded_rectangle([(tx, 120), (tx + tw, 210)], radius=14, fill=tier["border"])
        draw.rectangle([(tx, 180), (tx + tw, 210)], fill=tier["border"])
        draw.text((tx + 24, 135), tier["title"], fill=(255, 255, 255), font=get_font(20, bold=True))
        draw.text((tx + 24, 172), tier["subtitle"], fill=(241, 245, 249), font=get_font(15))

        # Module sub-boxes
        curr_y = 235
        for mod_title, mod_desc in tier["modules"]:
            draw.rounded_rectangle([(tx + 20, curr_y), (tx + tw - 20, curr_y + 150)], radius=10, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
            draw.rectangle([(tx + 20, curr_y), (tx + 28, curr_y + 150)], fill=tier["border"])
            draw.text((tx + 42, curr_y + 16), mod_title, fill=(15, 23, 42), font=get_font(17, bold=True))
            
            # Simple text wrap
            words = mod_desc.split(" ")
            line1, line2 = "", ""
            for w_str in words:
                if len(line1 + w_str) < 42:
                    line1 += w_str + " "
                else:
                    line2 += w_str + " "
            draw.text((tx + 42, curr_y + 54), line1.strip(), fill=(71, 85, 105), font=get_font(15))
            if line2:
                draw.text((tx + 42, curr_y + 82), line2.strip(), fill=(71, 85, 105), font=get_font(15))
            curr_y += 175

    # Connecting Flow Arrows between Tiers
    arrow_y_positions = [310, 485, 660, 835]
    for y_pos in arrow_y_positions:
        # Tier 1 -> Tier 2
        draw.line([(620, y_pos), (680, y_pos)], fill=(100, 116, 139), width=4)
        draw.polygon([(675, y_pos - 7), (675, y_pos + 7), (685, y_pos)], fill=(100, 116, 139))
        # Tier 2 -> Tier 3
        draw.line([(1240, y_pos), (1300, y_pos)], fill=(100, 116, 139), width=4)
        draw.polygon([(1295, y_pos - 7), (1295, y_pos + 7), (1305, y_pos)], fill=(100, 116, 139))

    img.save("slide7_architecture_blueprint.png", quality=95)
    print("Generated: slide7_architecture_blueprint.png")

if __name__ == "__main__":
    draw_slide6_langflow()
    draw_slide7_architecture()