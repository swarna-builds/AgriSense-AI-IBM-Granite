import time
from core.profile import FarmerProfile
from core.granite_engine import GraniteEngine
from core.prompts import build_agent_prompt
from services.weather_service import get_live_weather
from services.market_service import get_mandi_rates
from services.rag_service import AgriRAGService
from services.sentinel_daemon import SentinelDaemon

def main():
    print("--- [1/3] Initializing Sentinel Daemon (1s Tick) ---")
    profile = FarmerProfile(crop="Tomato", soil_type="Red Soil", crop_age_days=35)
    sentinel = SentinelDaemon()
    sentinel.start_monitoring(profile)
    time.sleep(2)  # Allow background daemon to evaluate first tick
    
    alert = sentinel.get_alert()
    if alert:
        print(f"🚨 ACTIVE SENTINEL ALERT: {alert['title']} [{alert['timestamp']}]")
        print(f"   Action: {alert['protection_steps'][0]}")
    else:
        print("🟢 Sentinel Status: Clear — No immediate hazards.")

    print("\n--- [2/3] Retrieving Context & Executing Granite Engine ---")
    rag = AgriRAGService()
    query = "Leaves turning yellow"
    docs = rag.retrieve_guidance(profile.crop, query)
    weather = get_live_weather(profile.lat, profile.lon)
    market = get_mandi_rates(profile.crop, profile.district)
    
    sys_p, usr_p = build_agent_prompt(profile, weather, market, docs, query)
    engine = GraniteEngine()
    result = engine.generate_decision(sys_p, usr_p, docs)

    print("\n--- [3/3] Granite Structured Decision Output ---")
    print(f"🌱 Summary: {result['crop_status_summary']}")
    print(f"📊 Risk Scores: {result['risk_scores']}")
    print(f"💡 Action Decision: {result['actionable_decision']}")
    print(f"⚖️ Simulation Choice: {result['decision_simulation']['selected']}")
    print(f"📚 Grounded Source: {result['grounded_sources'][0]}")
    print("\n🎉 Phase 3 Complete! Decision Engine and 24/7 Watcher are active and robust.")

if __name__ == "__main__":
    main()