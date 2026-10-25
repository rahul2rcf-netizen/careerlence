# CareerLens AI

[![Open the interactive demo](https://img.shields.io/badge/Live%20demo-Open%20CareerLens-0B6B5E?style=for-the-badge)](https://rahul2rcf-netizen.github.io/careerlence/)

The browser-only showcase uses fictional sample data and illustrative scores; it does not upload a resume. GitHub Pages deployment is configured, but the repository owner must first enable **Settings → Pages → Build and deployment → GitHub Actions**. Once enabled, this URL will serve the interactive demo.

**A job-specific resume review loop:** see the evidence in your current resume, identify role-specific gaps, generate an optional AI-edited draft, then compare the score before and after you review the changes.

CareerLens is designed to make the reasoning visible. It does not predict interviews, model a real applicant-tracking system (ATS), or measure a candidate's ability.

## What you can do

- Compare a PDF, DOCX, TXT, or pasted resume with one job description.
- Review matched skills alongside the text evidence that triggered each match.
- Inspect apparent missing skills and a concrete practice brief grounded in those gaps.
- Opt in to a Groq-hosted open-weight model for a job-specific rewrite, drawbacks, and improvement suggestions.
- Edit the draft and compare the original and revised ATS-style estimates using the same scoring formula.
- Download the analysis or reviewed resume as Markdown or TXT.
- Try the interface with the included synthetic example without an API key.

## Quick start

Python 3.11 or newer is required.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Select **Try the synthetic example**, then **Analyze this role** to explore the report and before/after workflow. The example is fictional and contains no real resume data.

## Optional AI resume enhancer

The enhancer uses Groq's OpenAI-compatible API with `openai/gpt-oss-20b`, an open-weight model. Groq currently offers a free tier with rate limits; quotas and model access can change. You can provide a key in the app's password field, or configure `GROQ_API_KEY` as an environment variable / Streamlit secret. Create a key at [Groq Console](https://console.groq.com/keys).

For local Streamlit secrets, create `.streamlit/secrets.toml` (it is ignored by Git) with:

```toml
GROQ_API_KEY = "your-key"
```

No API key is required to use local matching, view evidence, or try the synthetic example. AI enhancement stays disabled until a key is provided and the user explicitly opts in to sending the resume and job text to Groq. Do not add API keys to source files or commit them.

The model is instructed to preserve source facts and not invent qualifications, dates, metrics, or results. AI can still make mistakes: inspect every claim before using a draft. The original resume is kept intact until the user chooses **Use draft as my new resume**.

## Scoring

`score = 100 × (0.60 × required coverage + 0.15 × preferred coverage + 0.25 × TF-IDF cosine similarity)`.

The same local formula is applied to the original and the reviewed draft. Coverage counts distinct detected dictionary skills; TF-IDF measures word overlap. The estimate may increase when relevant wording is clearer, but this is not evidence of improved qualifications or an actual ATS score. Keyword presence does not prove competence.

## Privacy and limitations

Local analysis processes uploaded files in memory and does not send resume text to a model. If the user supplies an API key, checks the disclosure, and requests AI enhancement, the resume and job description are sent to Groq. Groq says inference inputs and outputs are not retained by default, with limited temporary logging possible for service reliability and abuse monitoring; read [Groq's data controls](https://console.groq.com/docs/your-data) before using it with personal data. Remove personal or confidential details you do not want to share.

No database is used by this application. Streamlit keeps current UI state for the active session. Scanned PDFs need OCR, which is not included. Skill detection uses a small English dictionary, job requirement grouping is a text heuristic, and TF-IDF can miss equivalent meanings. Review extracted text, classified requirements, evidence, and AI output.

## Development

```powershell
python -m pytest
python -m ruff check .
```

## Project structure

- `app.py`: Streamlit interface and analysis flow.
- `src/careerlens/analysis.py`: requirement heuristic and transparent scoring.
- `src/careerlens/ai_enhancer.py`: opt-in Groq request and response validation.
- `src/careerlens/extraction.py`: PDF, DOCX, and TXT extraction.
- `src/careerlens/skills.py`: skill vocabulary, aliases, and evidence detection.
- `src/careerlens/report.py`: Markdown report export.
- `tests/`: synthetic behavior checks.

