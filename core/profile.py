from dataclasses import dataclass

@dataclass
class FarmerProfile:
    crop: str
    soil_type: str
    crop_age_days: int
    district: str
    irrigation_type: str
    language: str = "en"

    def summary(self) -> str:
        return f"{self.crop} ({self.crop_age_days}d) | {self.soil_type} | {self.district} | {self.irrigation_type}"