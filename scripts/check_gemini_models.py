import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("=== GEMINI MODELS SUPPORTING generateContent ===")

for model in client.models.list():
    actions = getattr(model, "supported_actions", None) or []
    if "generateContent" in actions:
        print(model.name)
