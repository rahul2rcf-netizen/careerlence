# Architecture

CareerLens v1 is a single-process Streamlit application. UI code lives in `app.py`; extraction, skill detection, deterministic scoring/advice, and Markdown rendering are separate modules under `src/careerlens`. There is no persistent database, external model, API service, telemetry, or file retention feature.

Uploaded bytes are capped at 10 MiB and dispatched by extension to PyMuPDF, python-docx, or UTF-8 text decoding. Extracted content is normalized and shown for review. The analysis module detects taxonomy entries once per canonical skill, heuristically groups job skills into required/preferred sections, computes coverage and scikit-learn TF-IDF cosine similarity, then returns evidence snippets and textual recommendations.

When required skill gaps exist, the engine derives one bounded project brief from up to three detected gaps. It describes a problem, objective, scope, and evidence expected; it does not claim that the candidate has completed the project. Streamlit session state holds the result for the active interaction. Markdown export is generated from that result. A future API or database would add complexity without a requirement in this initial local workflow.

