import os
from google import genai

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]

PROMPT = """
در 150 تا 200 کلمه، به زبان فارسی و با لحن یک کتاب فنی مهندسی،
«تابع گرین» را برای دانشجوی مهندسی توضیح بده.
تعریف، ایده اصلی، و یک کاربرد عملی آن را بیان کن.
فقط متن فارسی تولید کن و از فرمول LaTeX استفاده نکن.
"""

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("=== REAL PERSIAN BOOK-TEXT GENERATION TEST ===", flush=True)

for model in MODELS:
    print(f"\nTEST: {model}", flush=True)

    try:
        response = client.models.generate_content(
            model=model,
            contents=PROMPT,
        )

        text = (response.text or "").strip()
        candidates = response.candidates or []

        if not text:
            print(
                f"FAILURE: {model} -> EMPTY VISIBLE TEXT",
                flush=True,
            )
            continue

        print(
            f"SUCCESS: {model} -> "
            f"chars={len(text)}, words={len(text.split())}",
            flush=True,
        )

        preview = text.replace("\n", " ")[:250]
        print(f"PREVIEW: {preview}", flush=True)

        if candidates:
            print(
                f"FINISH_REASON: "
                f"{getattr(candidates[0], 'finish_reason', None)}",
                flush=True,
            )

    except Exception as exc:
        print(
            f"FAILURE: {model} -> "
            f"{type(exc).__name__}: {exc}",
            flush=True,
        )
