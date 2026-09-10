from core.profile import FarmerProfile
from services.weather_service import get_live_weather

def main():
    print("Testing Farmer Profile...")
    profile = FarmerProfile()
    print("✅", profile.summary())

    print("\nTesting Weather Service...")
    weather = get_live_weather(profile.lat, profile.lon)
    print("✅ Live Weather Result:", weather)
    print("\n🎉 Base setup verified successfully!")

if __name__ == "__main__":
    main()