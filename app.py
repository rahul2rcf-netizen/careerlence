"""Streamlit interface for CareerLens AI."""

import streamlit as st
from careerlens.analysis import analyze
from careerlens.extraction import extract_upload
from careerlens.report import markdown

st.set_page_config(page_title="CareerLens AI", page_icon=None, layout="wide")
st.markdown(
    """<style>
.stApp {background:#f6f5f1;color:#17211d} h1,h2,h3 {font-family:Georgia,serif;letter-spacing:-.025em}
[data-testid="stMetric"] {background:white;padding:1rem;border-left:3px solid #316b59}
div[data-testid="stVerticalBlock"] > div:has(> div > .evidence) {border-bottom:1px solid #ddd}
</style>""",
    unsafe_allow_html=True,
)
st.title("CareerLens AI")
st.write(
    "Understand how your resume lines up with one job description. CareerLens highlights evidence in your document, surfaces apparent gaps, and explains its score. It does not predict hiring outcomes."
)
with st.expander("How this works", expanded=False):
    st.write(
        "A transparent skill dictionary checks exact aliases and word boundaries. The score combines required-skill coverage (60%), preferred-skill coverage (15%), and TF-IDF cosine similarity (25%). Review the extracted text and detected requirements: both extraction and grouping can miss context."
    )
uploaded = st.file_uploader(
    "Resume document",
    type=["pdf", "docx", "txt"],
    help="PDF, DOCX, or TXT; up to 10 MB. Image-only PDFs need OCR, which is not included.",
)
resume = st.text_area("Or paste resume text", height=180, placeholder="Paste resume text here")
if uploaded:
    try:
        resume = extract_upload(uploaded.name, uploaded.getvalue())
    except Exception as exc:
        st.error(str(exc))
if resume:
    st.text_area(
        "Text used for analysis — review for extraction errors", value=resume, height=180, disabled=True
    )
job = st.text_area(
    "Job description",
    height=250,
    placeholder="Paste the complete job description. Label sections such as ‘Required’ and ‘Preferred’ for clearer grouping.",
)
title = st.text_input("Role title (optional)", value="Role")
if st.button("Analyze alignment", type="primary"):
    try:
        result = analyze(resume, job, title or "Role")
        st.session_state["result"] = result
    except Exception as exc:
        st.error(str(exc))
if "result" in st.session_state:
    a = st.session_state["result"]
    st.divider()
    st.header("Analysis")
    st.metric("Document-to-job alignment", f"{a.score}/100")
    c1, c2, c3 = st.columns(3)
    c1.metric("Required skill coverage", f"{a.required_coverage}%")
    c2.metric("Preferred skill coverage", f"{a.preferred_coverage}%")
    c3.metric("Text similarity", f"{a.text_similarity}%")
    st.caption(
        "Score = 60% required coverage + 15% preferred coverage + 25% TF-IDF cosine similarity. It is document alignment, not a hiring probability or measure of ability."
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Matched with resume evidence")
        if not a.matches:
            st.write("No dictionary matches detected.")
        for s in a.matches:
            st.markdown(f"**{s.name}** · {s.category}\n\n> {s.evidence}")
        st.subheader("Other resume skills")
        st.write(", ".join(s.name for s in a.extra) or "None detected")
    with right:
        st.subheader("Detected requirements")
        st.write("**Required:** " + (", ".join(a.required) or "None classified"))
        st.write("**Preferred:** " + (", ".join(a.preferred) or "None classified"))
        st.subheader("Apparent gaps")
        st.write(", ".join(a.gaps) or "No apparent gaps in detected skills.")
        st.caption(
            "A gap means the skill was not detected in the text; it does not mean the candidate lacks the skill."
        )
    st.subheader("Resume-specific next steps")
    for item in a.recommendations:
        st.write("• " + item)
    st.subheader("Project idea grounded in this job")
    for project in a.projects:
        st.markdown(f"**{project['name']}**")
        st.write(project["problem"])
        st.write("**Technical objective:** " + project["objective"])
        st.write("**Relevant skills:** " + ", ".join(project["skills"]))
        st.write("**Minimum scope:** " + project["scope"])
        st.write("**Evidence to produce:** " + project["evidence"])
        st.caption(project["before_listing"])
    if not a.projects:
        st.write(
            "No detected skill gaps to ground a project suggestion in. Review the job requirements and resume text before choosing a project."
        )
    st.download_button(
        "Download analysis as Markdown", markdown(a), file_name="careerlens-analysis.md", mime="text/markdown"
    )
    st.caption(
        "Processed in this app session. No resume text is written to a database or external AI service by this application."
    )

