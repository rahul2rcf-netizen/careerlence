"""Opt-in resume rewrite using Groq's OpenAI-compatible chat API."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = "openai/gpt-oss-20b"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MAX_TEXT_CHARS = 12_000


def configured_api_key() -> str | None:
    """Read a configured Groq key without exposing it to the UI."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(__import__("streamlit").secrets.get("GROQ_API_KEY", "")).strip() or None
    except Exception:
        return None


def enhance_resume(resume: str, job: str, api_key: str) -> dict:
    """Return a truthful, role-targeted draft and improvement notes."""
    if not resume.strip() or not job.strip():
        raise ValueError("Provide both resume text and the target job description.")
    if len(resume) > MAX_TEXT_CHARS or len(job) > MAX_TEXT_CHARS:
        raise ValueError("For the free model, keep each text under 12,000 characters.")

    system = """You are a careful resume editor. Tailor the resume to the supplied job description using ONLY facts, skills, tools, dates, metrics, and accomplishments explicitly supported by the original resume. Never invent or infer qualifications, employers, dates, numbers, outcomes, certifications, or experience. Never add a job requirement as a claim unless it already appears in the resume. Preserve the candidate's meaning. You may reorder sections, improve clarity, and make existing evidence more specific without adding facts. Return valid JSON only with keys: enhanced_resume (string), improvements (array of short strings), drawbacks (array of short strings), unsupported_job_skills (array of strings). If a claim cannot be improved truthfully, flag it as a drawback rather than filling in a detail."""
    user = (
        "TARGET JOB DESCRIPTION:\n" + job.strip() + "\n\nORIGINAL RESUME (source of truth):\n" + resume.strip()
    )
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "max_tokens": 4500,
        "response_format": {"type": "json_object"},
    }
    request = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=75) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 429:
            raise RuntimeError("The free API rate limit was reached. Try again later.") from exc
        if exc.code in (401, 403):
            raise RuntimeError("The Groq API key was rejected. Check the key in your app settings.") from exc
        raise RuntimeError(f"The Groq API returned an error (HTTP {exc.code}). Try again later.") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError("Could not reach the Groq API. Check your connection and try again.") from exc
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("The model returned an unreadable response. Please try again.") from exc

    try:
        content = body["choices"][0]["message"]["content"]
        result = json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("The model did not return the expected resume draft.") from exc
    if not isinstance(result.get("enhanced_resume"), str) or not result["enhanced_resume"].strip():
        raise RuntimeError("The model did not return a resume draft.")
    for key in ("improvements", "drawbacks", "unsupported_job_skills"):
        if not isinstance(result.get(key), list):
            result[key] = []
    result["improvements"] = [str(item) for item in result["improvements"][:8]]
    result["drawbacks"] = [str(item) for item in result["drawbacks"][:8]]
    result["unsupported_job_skills"] = [str(item) for item in result["unsupported_job_skills"][:12]]
    return result

