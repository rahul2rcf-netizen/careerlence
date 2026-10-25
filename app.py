"""Streamlit interface for CareerLens AI."""

from pathlib import Path
import sys

import streamlit as st

# Make the src-layout package importable when running `streamlit run app.py`
# from a fresh environment installed with requirements.txt only.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from careerlens.analysis import analyze
from careerlens.extraction import extract_upload
from careerlens.report import markdown

st.set_page_config(page_title="CareerLens AI", page_icon="◉", layout="wide")

st.markdown(
    """<style>
    :root { --ink:#1b2926; --muted:#67736d; --paper:#f4f3ee; --card:#fffefa;
            --green:#216857; --mint:#dcebe4; --line:#dce1dc; --orange:#d98952; }
    .stApp { background:var(--paper); color:var(--ink); }
    [data-testid="stHeader"] { background:rgba(244,243,238,.92); }
    [data-testid="stMainBlockContainer"] { max-width:1180px; padding-top:2rem; }
    h1,h2,h3 { color:var(--ink); font-family:Georgia,serif; letter-spacing:-.035em; }
    h1 { font-size:3.2rem !important; line-height:1.02 !important; }
    h2 { margin-top:1rem; }
    p,li,label { color:var(--ink); }
    .eyebrow { color:var(--green); font-size:.72rem; font-weight:750; letter-spacing:.17em; text-transform:uppercase; }
    .hero { background:var(--card); border:1px solid var(--line); border-radius:5px; padding:2rem 2.2rem;
            margin:.4rem 0 1.5rem; position:relative; overflow:hidden; }
    .hero:after { content:""; position:absolute; right:-52px; top:-80px; width:260px; height:260px;
                  border:1px solid #d7e5dc; border-radius:50%; box-shadow:0 0 0 24px #eff4ef,0 0 0 25px #d7e5dc,0 0 0 52px #f6f7f2,0 0 0 53px #e5e8df; }
    .hero-copy { max-width:740px; position:relative; z-index:1; }
    .hero-copy p { color:var(--muted); font-size:1.06rem; line-height:1.6; }
    .step { color:var(--green); font-size:.72rem; font-weight:750; letter-spacing:.12em; text-transform:uppercase; margin:0 0 .35rem; }
    .section-card { background:var(--card); border:1px solid var(--line); padding:1.15rem 1.25rem; border-radius:4px; }
    [data-testid="stMetric"] { background:var(--card); border:1px solid var(--line); border-radius:4px; padding:1rem 1.1rem; }
    [data-testid="stMetricLabel"] { color:var(--muted); }
    [data-testid="stMetricValue"] { color:var(--green); font-family:Georgia,serif; }
    [data-testid="stProgressBar"] > div > div { background:var(--green); }
    .stButton > button[kind="primary"] { background:var(--green); border:1px solid var(--green); }
    .stButton > button { border-radius:3px; }
    [data-testid="stTabs"] button { color:var(--muted); }
    [data-testid="stAlert"] { border-radius:3px; }
    footer { visibility:hidden; }
    </style>
    <section class="hero"><div class="hero-copy">
    <div class="eyebrow">A clearer way to prepare</div>
    <h1>Make your next application more deliberate.</h1>
    <p>Compare your resume with one role. See what the document supports, what it may be missing, and how the match estimate is calculated. Your resume is analyzed in this session; it is not sent to an AI service.</p>
    </div></section>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### CareerLens AI")
    st.caption("Resume-to-role analysis")
    st.divider()
    st.markdown("**How the score works**")
    st.caption("60% required-skill coverage · 15% preferred-skill coverage · 25% TF-IDF text similarity")
    st.markdown("**A careful estimate**")
    st.caption(
        "This measures document alignment. It is not a hiring probability, a competence test, or a measure of your worth."
    )
    st.markdown("**Privacy**")
    st.caption("No database or external model is used. Uploaded files are processed in memory by this app.")

if st.button(
    "Try the synthetic example", help="Loads the sample resume and job description included with the project."
):
    sample_dir = Path(__file__).parent / "data" / "sample_inputs"
    st.session_state.resume_text = (sample_dir / "resume.txt").read_text(encoding="utf-8")
    st.session_state.job_text = (sample_dir / "job.txt").read_text(encoding="utf-8")
    st.session_state.role_title = "Junior Data Engineer"
    st.session_state.upload_signature = None
    st.session_state.pop("analysis_result", None)

st.markdown('<div class="step">01 / Your materials</div>', unsafe_allow_html=True)
col_resume, col_job = st.columns([1, 1.15], gap="large")
with col_resume:
    st.subheader("Resume")
    uploaded = st.file_uploader(
        "Upload PDF, DOCX, or TXT",
        type=["pdf", "docx", "txt"],
        help="Maximum 10 MB. Scanned image PDFs need OCR, which is not included.",
    )
    if uploaded:
        signature = (uploaded.name, uploaded.size)
        if st.session_state.get("upload_signature") != signature:
            try:
                st.session_state.resume_text = extract_upload(uploaded.name, uploaded.getvalue())
                st.session_state.upload_signature = signature
            except Exception as exc:
                st.error(str(exc))
    resume = st.text_area(
        "Extracted text · review and edit before analysis",
        key="resume_text",
        height=280,
        placeholder="Upload a document or paste your resume text. You can correct the extracted text here.",
    )
    st.caption("Your edits are used in the analysis. No original file is retained by the app.")

with col_job:
    st.subheader("Target role")
    title = st.text_input("Role title", key="role_title", placeholder="e.g. Junior Data Engineer")
    job = st.text_area(
        "Job description",
        key="job_text",
        height=280,
        placeholder="Paste the full job description. Label sections ‘Required’ and ‘Preferred’ for clearer grouping.",
    )
    st.caption(
        "Review the detected requirements after analysis. Mentioning a skill in an advert does not always make it mandatory."
    )

st.markdown('<div class="step">02 / Read the match</div>', unsafe_allow_html=True)
analyze_col, report_col = st.columns([1, 3])
with analyze_col:
    run_analysis = st.button("Analyze this role", type="primary", use_container_width=True)
if run_analysis:
    try:
        st.session_state.analysis_result = analyze(resume, job, title or "Role")
    except Exception as exc:
        st.error(str(exc))

if "analysis_result" in st.session_state:
    result = st.session_state.analysis_result
    st.divider()
    st.markdown('<div class="step">03 / Your analysis</div>', unsafe_allow_html=True)
    st.title(result.title)
    st.caption("Estimated document-to-job alignment")
    st.progress(result.score / 100, text=f"{result.score} / 100")

    m1, m2, m3 = st.columns(3, gap="medium")
    m1.metric("Required skill coverage", f"{result.required_coverage}%")
    m2.metric("Preferred skill coverage", f"{result.preferred_coverage}%")
    m3.metric("Text similarity", f"{result.text_similarity}%")
    st.caption(
        "Formula: 60% required coverage + 15% preferred coverage + 25% TF-IDF cosine similarity. A high score does not guarantee suitability or selection."
    )

    overview, evidence, next_steps = st.tabs(["At a glance", "Skills & evidence", "Improve before applying"])
    with overview:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("#### Detected job requirements")
            st.write("**Required**")
            st.write(", ".join(result.required) or "No required skills classified")
            st.write("**Preferred**")
            st.write(", ".join(result.preferred) or "No preferred skills classified")
        with right:
            st.markdown("#### Apparent document gaps")
            if result.gaps:
                st.write(" · ".join(result.gaps))
            else:
                st.write("No gaps found in the skills covered by this dictionary.")
            st.info(
                "A gap means a skill wasn’t detected in the supplied text. It doesn’t mean you lack the skill."
            )
    with evidence:
        if result.matches:
            for skill in result.matches:
                with st.expander(f"{skill.name}  ·  {skill.category}", expanded=True):
                    st.write(skill.evidence)
        else:
            st.info(
                "No shared dictionary skills detected yet. Check the text above and expand the skill taxonomy if needed."
            )
        st.markdown("**Other skills in your resume**")
        st.write(", ".join(skill.name for skill in result.extra) or "None detected")
        st.caption("Dictionary matches show text evidence, not proof of proficiency.")
    with next_steps:
        st.markdown("#### Resume-specific edits")
        for recommendation in result.recommendations:
            st.markdown(f"- {recommendation}")
        st.markdown("#### A project brief based on this role")
        if result.projects:
            project = result.projects[0]
            st.markdown(f"**{project['name']}**")
            st.write(project["problem"])
            st.write("**Objective:** " + project["objective"])
            st.write("**Skills:** " + ", ".join(project["skills"]))
            st.write("**Minimum scope:** " + project["scope"])
            st.write("**Evidence to produce:** " + project["evidence"])
            st.caption(project["before_listing"])
        else:
            st.write(
                "No skill gap was detected to ground a project brief in. Review the job text and choose a real problem before starting a project."
            )

    with report_col:
        st.download_button(
            "Download this analysis · Markdown",
            markdown(result),
            file_name="careerlens-analysis.md",
            mime="text/markdown",
        )

    with st.expander("Limitations and scoring details"):
        st.write(
            "Skill detection uses a small English-language dictionary and exact aliases. Job requirement grouping is a text heuristic. TF-IDF measures word overlap and can miss equivalent meanings. Review the resume text, detected requirements, and evidence before acting on the score."
        )
else:
    st.markdown("---")
    st.markdown("### A useful result starts with the actual wording")
    st.write(
        "Add one resume and the full job description. CareerLens will point to the text that supports each detected match so you can review the reasoning—not just a number."
    )

