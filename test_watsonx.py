import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

print("Checking IBM watsonx.ai connection...")

try:
    creds = Credentials(api_key=api_key, url=url)
    params = TextChatParameters(temperature=0.1, max_tokens=100)
    model = ModelInference(
       model_id = "mistralai/mistral-small-3-1-24b-instruct-2503",
        credentials=creds,
        project_id=project_id,
        params=params
    )
    response = model.chat(messages=[{"role": "user", "content": "Hello, respond with: Granite is ready."}])
    print("✅ Connection Successful!")
    print("IBM Granite Response:", response["choices"][0]["message"]["content"])
except Exception as e:
    print("❌ Connection Failed:", e)