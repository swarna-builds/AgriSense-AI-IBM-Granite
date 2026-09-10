import logging
from typing import Optional

class SentinelDaemon:
    """Instantaneous Crop-Risk Sentinel Engine.
    Evaluates Agromet risk in 0ms without blocking UI rendering or exhausting API rate limits.
    """

    def __init__(self):
        self.current_alert = None

    def start_monitoring(self, profile):
        pass

    def evaluate_risk(self, profile, weather: dict, rag_service=None, engine=None) -> Optional[dict]:
        """Evaluates live biological risk thresholds based on verified university advisories."""
        crop_str = str(getattr(profile, "crop", "")).lower()
        loc = getattr(profile, "district", "Field")
        
        hum = weather.get("humidity", 50)
        rain = weather.get("rain_prob", 0)
        temp = weather.get("temperature", 28.0)

        # 1. GRAPES (Bangalore Blue / Commercial Vineyards)
        if any(g in crop_str for g in ["grape", "grapes", "ದ್ರಾಕ್ಷಿ", "ద్రాಕ್ಷ", "अंगूर"]):
            if hum >= 78 or rain >= 35:
                return {
                    "risk_level": "HIGH",
                    "title": "Grapes Downy Mildew Red Risk Alert (UAS Bangalore Advisory)",
                    "message": f"Critical humidity ({hum}%) detected at {loc}. High vulnerability to Downy Mildew (Plasmopara viticola).",
                    "protection_steps": [
                        "CRITICAL: Suspend all pruning, shoot thinning, and growth regulator sprays immediately (wounds allow fungal entry).",
                        "Spray 1% Bordeaux Mixture or Metalaxyl + Mancozeb (Ridomil Gold) @ 2 g/L of water.",
                        "Thin dense lower foliage to optimize canopy air movement and accelerate drying."
                    ]
                }
            return None

        # 2. TOMATO & HORTICULTURAL CROPS
        elif any(v in crop_str for v in ["tomato", "potato", "ಟೊಮೇಟೊ", "టమోటా", "टमाटर"]):
            if hum >= 75 or (hum >= 68 and rain >= 30):
                return {
                    "risk_level": "HIGH",
                    "title": "Tomato Late Blight & Fruit Rot Alert (KVK Advisory)",
                    "message": f"Elevated humidity ({hum}%) creates favorable conditions for Late Blight and Anthracnose at {loc}.",
                    "protection_steps": [
                        "Suspend flood and overhead sprinkler irrigation immediately to avoid canopy wetness.",
                        "Spray Metalaxyl 8% + Mancozeb 64% (Ridomil Gold) @ 2 g/L or Azoxystrobin @ 1 ml/L.",
                        "Ensure deep drainage trenches between raised beds to clear excess root moisture."
                    ]
                }
            return None

        # 3. ARECANUT & BLACK PEPPER
        elif any(c in crop_str for c in ["arecanut", "betel nut", "adike", "vakka"]):
            if hum >= 85 and (rain >= 40 or temp <= 28):
                return {
                    "risk_level": "HIGH",
                    "title": "Arecanut Koleroga (Fruit Rot) High Alert",
                    "message": f"Continuous humidity ({hum}%) fosters Phytophthora nut dropping at {loc}.",
                    "protection_steps": [
                        "Spray 1% Bordeaux Mixture with resin sticker (1 ml/L) thoroughly on all nut bunches.",
                        "Tie protective polythene covers over maturing bunches if rains persist."
                    ]
                }
            return None

        # 4. CHILLI
        elif any(c in crop_str for c in ["chilli", "mirchi", "మిరప", "ಮೆಣಸಿನಕಾಯಿ"]):
            if hum >= 75 or rain >= 35:
                return {
                    "risk_level": "HIGH",
                    "title": "Chilli Anthracnose & Die-back Alert",
                    "message": f"Warm, wet air ({hum}%) causes rapid blossom drop and twig die-back.",
                    "protection_steps": [
                        "Spray Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L of water.",
                        "Open drainage lines to clear stagnant water."
                    ]
                }
            return None

        # 5. GENERAL MODERATE WATCH (For other crops under dampness)
        elif hum >= 75 or rain >= 40:
            crop_name = getattr(profile, "crop", "Crop").split(' ')[0]
            return {
                "risk_level": "MODERATE",
                "title": f"{crop_name} Moderate Weather Watch",
                "message": f"Elevated humidity ({hum}%) detected at {loc}. Elevated fungal and sucking pest pressure.",
                "protection_steps": [
                    "Inspect lower leaves for early fungal spots or pest nymphs.",
                    "Apply prophylactic Neem Oil (10,000 PPM @ 3 ml/L) to prevent spore establishment."
                ]
            }

        return None

    def get_alert(self):
        return self.current_alert