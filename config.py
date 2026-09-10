import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # watsonx Configuration
    WATSONX_APIKEY = os.getenv("WATSONX_APIKEY", "")
    WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
    WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    GRANITE_MODEL_ID = "ibm/granite-3-8b-instruct"
    
    # External API Keys
    DATA_GOV_APIKEY = os.getenv("DATA_GOV_APIKEY", "")
    
    # Cache Timers (in seconds)
    WEATHER_CACHE_TTL = 10800   # 3 Hours
    MARKET_CACHE_TTL = 43200    # 12 Hours
    SENTINEL_COOLDOWN = 14400   # 4 Hours between risk notifications
    
    # Mode switch
    MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"