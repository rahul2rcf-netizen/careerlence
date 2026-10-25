# CareerLens AI

CareerLens AI is a local-first, explainable resume-to-job alignment tool for early-career applicants. It helps answer which listed requirements appear in a resume, where the document supports those matches, and which terms were not detected. It does not predict hiring outcomes or measure a person's ability.

## Features

- PDF, DOCX, and TXT extraction plus pasted text; extracted resume text can be reviewed.
- Editable extracted resume text, a synthetic sample workflow, and a compact three-part results view.
- Dictionary-based skill extraction with aliases, categories, evidence snippets, and word boundaries.
- Required and preferred coverage, TF-IDF cosine similarity, visible score components, and apparent gaps.
- Resume-specific wording suggestions, gap-grounded project scope, and Markdown report export.
- Local processing without an external model API or database.

## Install and run

Python 3.11 or newer is required. From the project directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Optional hosted demo

The app is ready to deploy from this repository with Streamlit Community Cloud: select the repository's `main` branch and `app.py` as the entry point. Hosting requires an account on that service. No live deployment URL is published by this project yet.

## Tests and quality

```powershell
python -m pytest
python -m ruff check .
```

The repository includes synthetic tests for aliases, false-positive boundaries, duplicate skill mentions, coverage, evidence, zero-vector behavior, input validation, normalization, and report export. The `data/sample_inputs/` pair is synthetic and can be pasted into the app. No real resume data is included.

## Scoring methodology

`score = 100 × (0.60 × required coverage + 0.15 × preferred coverage + 0.25 × TF-IDF cosine similarity)`.

Coverage is the share of distinct dictionary skills in a group also detected in the resume. If a group has no detected items, its coverage is zero. TF-IDF is computed over the two supplied texts with English stop words; empty vocabularies yield zero. The result is clamped by its components to 0–100. Exact weights are visible in the interface. Keyword presence is not proof of competence, and text similarity can reward generic overlap.

## Sample workflow

Start the app, select **Try the synthetic example**, and click **Analyze this role**. Explore the overview, skills and evidence, and improvement tabs. Upload your own supported resume file or paste resume text, edit the extracted text if needed, then paste a job description and analyze again. The included sample documents are fictional and contain no real candidate data.

## Architecture

- `app.py`: Streamlit input and result presentation.
- `src/careerlens/extraction.py`: upload validation, extraction, and whitespace normalization.
- `src/careerlens/skills.py`: editable skill taxonomy and evidence detection.
- `src/careerlens/analysis.py`: requirement heuristic, scoring, and grounded recommendations.
- `src/careerlens/report.py`: Markdown export.
- `tests/`: synthetic unit checks.

## Evaluation

Automated tests provide behavioral checks, not predictive quality metrics. No manually reviewed benchmark has been run, so precision, recall, and F1 are not claimed. Before relying on this tool for broader comparisons, curate and manually label a representative dataset of resume/job pairs, then report per-skill extraction precision/recall and gap error counts. The dictionary and section heuristic are currently narrow and English-centric.

## Privacy and limitations

Files are read from the upload in memory and are not saved by the app. No resume text is logged or sent to an external AI provider. Streamlit session state keeps the current analysis while the session is active; users should run the app on a trusted local machine. This is not a formal security audit. Scanned PDFs need OCR, which is not included. Password-protected or damaged files may fail extraction. Skill coverage is limited to the maintained dictionary; requirement grouping uses section words and may need manual correction. Any suggested project brief is based on detected gaps; candidates should only list it after doing the work.

## Future work

Improve editable requirement extraction, grow the taxonomy with reviewed examples, and evaluate against a manually labeled dataset before considering semantic embeddings. A deployment should follow a privacy and hosting review.

