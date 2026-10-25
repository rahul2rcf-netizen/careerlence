"""Deterministic scoring, requirement parsing, and evidence-led advice."""

import re
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .skills import detect_skills


@dataclass
class Analysis:
    score: float
    required_coverage: float
    preferred_coverage: float
    text_similarity: float
    resume_skills: list
    job_skills: list
    required: list
    preferred: list
    matches: list
    gaps: list
    extra: list
    recommendations: list
    projects: list
    title: str


def _requirements(job: str) -> tuple[list[str], list[str]]:
    required, preferred = [], []
    mode = "required"
    for line in job.splitlines():
        low = line.lower()
        if re.search(r"preferred|nice to have|bonus|optional", low):
            mode = "preferred"
        elif re.search(r"required|must have|qualifications", low):
            mode = "required"
        for skill in detect_skills(line, "job"):
            target = preferred if mode == "preferred" else required
            if skill.name not in target:
                target.append(skill.name)
    return required, preferred


def analyze(resume: str, job: str, title: str = "Role") -> Analysis:
    resume, job = resume.strip(), job.strip()
    if not resume or not job:
        raise ValueError("Provide both resume text and a job description.")
    rs, js = detect_skills(resume, "resume"), detect_skills(job, "job")
    rnames, jnames = {s.name for s in rs}, {s.name for s in js}
    required, preferred = _requirements(job)
    req_cov = len(rnames & set(required)) / len(required) if required else 0.0
    pref_cov = len(rnames & set(preferred)) / len(preferred) if preferred else 0.0
    try:
        similarity = float(
            cosine_similarity(TfidfVectorizer(stop_words="english").fit_transform([resume, job]))[0, 1]
        )
    except ValueError:
        similarity = 0.0
    score = 100 * (0.60 * req_cov + 0.15 * pref_cov + 0.25 * similarity)
    matches = [s for s in rs if s.name in jnames]
    gaps = [n for n in required + preferred if n not in rnames]
    extra = [s for s in rs if s.name not in jnames]
    recs = []
    for name in required:
        if name not in rnames:
            recs.append(
                f"{name} is an apparent document gap. If you have used it, add the specific project or coursework evidence; otherwise build and document a small example before listing it."
            )
    for line in resume.splitlines():
        clean = line.strip(" •-*\t")
        if len(clean) > 35 and not re.search(
            r"\b(built|implemented|designed|developed|trained|deployed|created|evaluated)\b", clean, re.I
        ):
            recs.append(
                f"This resume line describes activity without a clear implementation verb: ‘{clean[:180]}’. Clarify what you personally built and the tools used, using only accurate details."
            )
            break
    if not recs:
        recs.append(
            "Your text includes implementation-oriented wording. Check that each technical claim has a concrete project, coursework, or work example behind it."
        )
    projects = []
    if gaps:
        focus = gaps[:3]
        projects.append(
            {
                "name": f"Role-focused {title} prototype",
                "problem": "Build a small, reproducible solution to a problem described in the supplied job posting.",
                "objective": f"Demonstrate a working workflow that uses {', '.join(focus)} in context, rather than listing the terms alone.",
                "skills": focus,
                "scope": "Choose one realistic input, implement the core workflow, add validation and tests, and document setup and trade-offs. Keep scope to a weekend-sized prototype.",
                "evidence": "A public or locally demonstrable repository with runnable instructions, tests, a short design note, and a truthful explanation of your contribution.",
                "before_listing": "Implement and verify the project yourself. Only list technologies and results you can explain; do not add it to your resume before the evidence exists.",
            }
        )
    return Analysis(
        round(score, 1),
        round(req_cov * 100, 1),
        round(pref_cov * 100, 1),
        round(similarity * 100, 1),
        rs,
        js,
        required,
        preferred,
        matches,
        gaps,
        extra,
        recs,
        projects,
        title,
    )

