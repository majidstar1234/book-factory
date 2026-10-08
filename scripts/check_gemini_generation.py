import os
from google import genai

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("=== DEEP GEMINI generateContent TEST ===", flush=True)

for model in MODELS:
    print(f"\nTEST: {model}", flush=True)

    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: OK",
        )

        response_text = (response.text or "").strip()
        candidates = response.candidates or []

        print(f"CANDIDATES: {len(candidates)}", flush=True)

        for index, candidate in enumerate(candidates, start=1):
            print(
                f"CANDIDATE {index} FINISH_REASON: "
                f"{getattr(candidate, 'finish_reason', None)}",
                flush=True,
            )

            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) or []

            print(f"CANDIDATE {index} PARTS: {len(parts)}", flush=True)

            for part_index, part in enumerate(parts, start=1):
                part_text = getattr(part, "text", None)
                thought = getattr(part, "thought", None)

                print(
                    f"PART {part_index}: "
                    f"thought={thought!r}, text={part_text!r}",
                    flush=True,
                )

        if response_text:
            print(
                f"SUCCESS: {model} -> {response_text!r}",
                flush=True,
            )
        else:
            print(
                f"FAILURE: {model} -> EMPTY VISIBLE TEXT",
                flush=True,
            )

    except Exception as exc:
        print(
            f"FAILURE: {model} -> "
            f"{type(exc).__name__}: {exc}",
            flush=True,
        )
