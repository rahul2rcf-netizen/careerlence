# CareerLens AI

> Evidence-led resume-to-role review. Understand what matches, find document gaps, and improve a draft while keeping every claim yours.

[![Open demo](https://img.shields.io/badge/Interactive%20demo-Open%20CareerLens-0B6B5E?style=for-the-badge)](https://rahul2rcf-netizen.github.io/careerlence/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

**Pages status:** the demo files and automated deployment workflow are in this repository. GitHub Pages still needs to be enabled once by the repository owner: open **Settings → Pages → Build and deployment → Source → GitHub Actions**. Then re-run the **Deploy CareerLens showcase to GitHub Pages** workflow from the Actions tab. The link above will work after a successful deployment.

CareerLens is a practical resume review workspace for one target role at a time. It connects job requirements to text evidence in a resume, makes the score components visible, and provides a human-reviewed improvement loop. It does **not** predict interviews, represent a real applicant-tracking system, or measure a candidate's ability.

## Project at a glance

| Area | What it does |
| --- | --- |
| Role matching | Compares a resume with one job description and separates detected required and preferred skills. |
| Evidence | Shows resume text snippets that triggered each detected skill, so matches can be checked. |
| Gap review | Lists role terms not detected in the document and provides a grounded next-step brief. |
| Resume enhancement | Offers optional AI-assisted rewriting, drawbacks, and improvement suggestions through Groq. |
| Before/after review | Recalculates the same ATS-style estimate for the original and the edited draft. |
| Export | Downloads a Markdown report or a plain-text reviewed draft. |
| Synthetic preview | Lets visitors explore the interaction without uploading a resume, adding a key, or calling an AI service. |

## Two ways to explore CareerLens

### 1. Interactive browser showcase

The static website in `docs/` is designed for a quick portfolio demo. It includes an editable synthetic resume and job posting, a browser-side match report, tabs for skills and gaps, evidence, and improvement guidance, plus an illustrative rewrite and before/after estimate.

- Uses fictional example text.
- Runs locally in the browser; it sends no resume or job text to a server.
- Uses a compact term dictionary and similarity calculation for the demo.
- Does not call an AI model and is not the full Python analysis engine.

After GitHub Pages is enabled, open the **Interactive demo** badge above.

To preview the static showcase locally:

```powershell
py -m http.server 8000 --directory docs
```

Then visit [http://localhost:8000](http://localhost:8000).

### 2. Full Streamlit application

#### Requirements

- Python 3.11 or newer
- Packages in `requirements.txt`
- Optional Groq API key only for AI enhancement

#### Install and run

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**macOS / Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

#### Recommended walkthrough

1. Choose **Try the synthetic example** to load fictional resume and role data.
2. Select **Analyze this role**.
3. Review the score components, matched requirements, evidence snippets, and apparent gaps.
4. Open the report and verify the extracted text and requirement grouping before acting on it.
5. If you have configured a Groq key and want AI help, explicitly opt in to the disclosure and generate an enhanced draft.
6. Read the model's drawbacks and suggestions. Edit the draft so every statement remains accurate.
7. Compare the original and revised estimates. Choose **Use draft as my new resume** only when you accept the changes.
8. Download the analysis or reviewed draft if useful.

You can also paste resume text directly, or upload PDF, DOCX, or TXT files. Scanned PDFs require OCR, which is not included.

## AI resume enhancer (optional)

The enhancer uses Groq's OpenAI-compatible API with the open-weight `openai/gpt-oss-20b` model. It can draft role-specific wording, flag unsupported requirements, and offer improvement suggestions. Check the provider's current model availability and limits before use.

1. Create a key in the [Groq Console](https://console.groq.com/keys).
2. Enter it in the app's password field, or configure it as an environment variable / Streamlit secret.
3. Keep the explicit consent checkbox selected only when you want to send resume and job text to Groq.
4. Check every generated claim against the original resume.

For local Streamlit secrets, create `.streamlit/secrets.toml` (ignored by Git) with:

```toml
GROQ_API_KEY = "your-key"
```

Or copy `.env.example` and configure the key in your environment. **Never commit API keys.** The local matcher, evidence view, synthetic example, and static showcase work without a key.

The model is instructed not to invent credentials, dates, metrics, or results, but AI can still be wrong. The original resume remains intact unless you choose to apply the reviewed draft.

## How the estimate works

The full application uses the same formula for the original and revised text:

```
score = 100 × (
    0.60 × required skill coverage
  + 0.15 × preferred skill coverage
  + 0.25 × TF-IDF cosine similarity
)
```

Coverage counts distinct skills recognized by the project's dictionary. TF-IDF estimates text overlap. The estimate may change when wording is clearer, but it is **not an actual ATS score, hiring prediction, or evidence of stronger qualifications**. Keyword presence does not prove competence. See [scoring methodology](docs/scoring-methodology.md).

## Privacy and limitations

- The full app processes local uploads in memory and does not send text to an AI model during normal matching.
- When you provide a Groq key, explicitly opt in, and request enhancement, the resume and job description are sent to Groq. Review [Groq's data controls](https://console.groq.com/docs/your-data) before using personal information.
- No database is used. Streamlit holds UI state for the active session.
- Skill detection uses a limited English vocabulary. Requirement grouping is heuristic and TF-IDF can miss equivalent wording.
- Review extracted text, evidence, requirement grouping, and every AI-generated claim.

## Development

```powershell
python -m pytest
python -m ruff check .
```

## Repository map

- `app.py` — Streamlit interface and review workflow.
- `src/careerlens/analysis.py` — requirement grouping and transparent score.
- `src/careerlens/ai_enhancer.py` — opt-in Groq call and response validation.
- `src/careerlens/extraction.py` — PDF, DOCX, and TXT text extraction.
- `src/careerlens/skills.py` — skill aliases, detection, and evidence.
- `src/careerlens/report.py` — Markdown report export.
- `docs/` — static showcase, scoring notes, architecture, and evaluation notes.
- `tests/` — synthetic behavior checks.

## License

See [LICENSE](LICENSE) if present in this repository.
