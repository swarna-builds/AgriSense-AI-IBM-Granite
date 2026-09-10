from core.profile import FarmerProfile
from core.prompts import build_agent_prompt
from services.weather_service import get_live_weather
from services.market_service import get_mandi_rates
from services.rag_service import AgriRAGService

def main():
    print("--- [1/3] Loading Profile & Telemetry ---")
    profile = FarmerProfile(crop="Tomato", soil_type="Red Soil", crop_age_days=35)
    weather = get_live_weather(profile.lat, profile.lon)
    market = get_mandi_rates(profile.crop, profile.district)
    print(f"✅ Weather: {weather['temperature']}°C, Humidity: {weather['humidity']}%, Rain: {weather['rain_prob']}%")
    print(f"✅ Mandi Price: ₹{market['modal_price']}/Qtl ({market['market']})")

    print("\n--- [2/3] Retrieving ICAR Knowledge via RAG ---")
    rag = AgriRAGService()
    query = "Leaves are turning yellow with brown spots"
    docs = rag.retrieve_guidance(profile.crop, query)
    print(f"✅ Retrieved {len(docs)} verified ICAR document(s):")
    for d in docs:
        print(f"   • {d['topic']} ({d['source']})")

    print("\n--- [3/3] Generating Grounded Granite Context ---")
    sys_p, usr_p = build_agent_prompt(profile, weather, market, docs, query)
    print("✅ System Prompt Ready.")
    print("✅ Context Payload Built Successfully.")
    print("\n🎉 Phase 2 Verified! RAG, Market data, and Prompts are fully integrated.")

if __name__ == "__main__":
    main()