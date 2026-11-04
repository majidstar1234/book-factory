from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from google import genai

ROOT = Path(__file__).resolve().parents[3]
PROMPT_PATH = ROOT / "research" / "active-systems-lab" / "prompts" / "vanderpol_parameter_study.md"
OUTPUT_DIR = ROOT / "research" / "active-systems-lab" / "results"


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is not set; refusing to call Gemini.")

    model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash").strip()
    if not model:
        raise SystemExit("GEMINI_MODEL is empty.")

    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    client = genai.Client(api_key=api_key)

    print(f"Sending research prompt to model: {model}", flush=True)
    response = client.models.generate_content(model=model, contents=prompt)
    answer = (response.text or "").strip()
    if not answer:
        raise SystemExit("Gemini returned no visible text; inspect provider response metadata.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "provider": "Google Gemini API",
        "model": model,
        "timestamp_utc": timestamp,
        "prompt_path": str(PROMPT_PATH.relative_to(ROOT)).replace("\\", "/"),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "response_text": answer,
    }
    out = OUTPUT_DIR / f"gemini_vanderpol_{timestamp}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved response artifact: {out.relative_to(ROOT)}", flush=True)
    print(f"Response characters: {len(answer)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
