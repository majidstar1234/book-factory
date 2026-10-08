import os
from google import genai
from google.genai import types

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("=== REAL GEMINI generateContent TEST ===")

for model in MODELS:
    print(f"\nTEST: {model}", flush=True)
    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: OK",
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=16,
            ),
        )

        text = (response.text or "").strip()
        print(f"SUCCESS: {model} -> {text!r}", flush=True)

    except Exception as exc:
        print(
            f"FAILURE: {model} -> {type(exc).__name__}: {exc}",
            flush=True,
        )
