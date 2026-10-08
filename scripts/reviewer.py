from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

from google import genai

ROOT = Path(__file__).resolve().parents[1]
OUTLINE_PATH = ROOT / "book" / "outline.json"
CHAPTERS_DIR = ROOT / "book" / "chapters"
REVIEWS_DIR = ROOT / "book" / "reviews"
REVIEW_PROMPT = (ROOT / "prompts" / "review.txt").read_text(encoding="utf-8")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip() or "gemini-3.8-flash"
FALLBACK_MODELS = tuple(
    m.strip()
    for m in os.getenv(
        "GEMINI_FALLBACK_MODELS",
        "gemini-3.7-flash,gemini-3.6-flash,gemini-3.5-flash",
    ).split(",")
    if m.strip()
)
MODEL_CHAIN = tuple(dict.fromkeys((MODEL, *FALLBACK_MODELS)))
MAX_RETRIES = max(1, int(os.getenv("GEMINI_MAX_RETRIES", "3")))
RETRY_DELAY = max(0, float(os.getenv("GEMINI_RETRY_DELAY", "5")))


def load_outline() -> dict[str, Any]:
    return json.loads(OUTLINE_PATH.read_text(encoding="utf-8"))


def save_outline(outline: dict[str, Any]) -> None:
    OUTLINE_PATH.write_text(
        json.dumps(outline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def choose(outline: dict[str, Any]) -> dict[str, Any] | None:
    requested = os.getenv("CHAPTER_ID", "").strip()
    if requested:
        cid = int(requested)
        candidates = [c for c in outline["chapters"] if int(c["id"]) == cid]
    else:
        candidates = outline["chapters"]

    for ch in candidates:
        if ch.get("status") == "written" and ch.get("review") == "pending":
            return ch
    return None


def generate_review(client: genai.Client, prompt: str) -> dict[str, Any]:
    last_error: Exception | None = None
    for model_name in MODEL_CHAIN:
        print(f"Gemini model: {model_name}", flush=True)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if not response.text:
                    raise RuntimeError("Reviewer returned an empty response")
                return extract_json(response.text)
            except Exception as exc:
                last_error = exc
                print(f"Gemini attempt {attempt}/{MAX_RETRIES} failed: {exc}", flush=True)
                if attempt < MAX_RETRIES:
                    delay = RETRY_DELAY * attempt
                    print(f"Retrying in {delay:g}s...", flush=True)
                    time.sleep(delay)
    raise RuntimeError("Reviewer failed after all configured Gemini models and retries") from last_error

def main() -> None:
    outline = load_outline()
    chapter = choose(outline)
    if chapter is None:
        print("No chapter needs review.")
        return

    path = CHAPTERS_DIR / f"chapter_{int(chapter['id']):03d}.md"
    content = path.read_text(encoding="utf-8")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)
    prompt = REVIEW_PROMPT.replace("{chapter_title}", chapter["title"]).replace("{chapter_content}", content)
    review = generate_review(client, prompt)

    score = int(review.get("score", 0))
    approved = bool(review.get("approved", False)) and score >= 75
    review["approved"] = approved
    review["score"] = score
    review["chapter_id"] = int(chapter["id"])

    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    out = REVIEWS_DIR / f"review_{int(chapter['id']):03d}.json"
    out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    chapter["review"] = "approved" if approved else "revision_required"
    chapter["status"] = "approved" if approved else "revision_required"
    chapter["review_score"] = score
    chapter.pop("last_error", None)
    save_outline(outline)
    print(f"Review saved to {out}; score={score}; status={chapter['status']}")


if __name__ == "__main__":
    main()
