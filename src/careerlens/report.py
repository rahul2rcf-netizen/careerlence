"""Markdown report export."""


def markdown(a) -> str:
    def skills(xs):
        return ", ".join(xs) if xs else "None detected"

    lines = [
        "# CareerLens AI analysis",
        f"\n**Role:** {a.title}",
        f"\n**Document-to-job alignment:** {a.score}/100",
        "\nThis estimates text alignment, not hiring probability, competence, or selection.",
        "\n## Score components",
        f"\n- Required skills: {a.required_coverage}%",
        f"- Preferred skills: {a.preferred_coverage}%",
        f"- TF-IDF text similarity: {a.text_similarity}%",
        "\nFormula: 60% required-skill coverage + 15% preferred-skill coverage + 25% TF-IDF cosine similarity.",
        "\n## Evidence-backed matches",
    ]
    lines += [f"\n- **{s.name}** — “{s.evidence}”" for s in a.matches] or ["\n- None detected"]
    lines += [
        "\n## Apparent gaps",
        "\n" + skills(a.gaps),
        "\nThese skills were not detected in the supplied resume text; this does not establish that the candidate lacks them.",
        "\n## Other detected resume skills",
        "\n" + skills([s.name for s in a.extra]),
        "\n## Recommendations",
    ]
    lines += [f"\n- {r}" for r in a.recommendations]
    lines += ["\n## Project suggestion"]
    for p in a.projects:
        lines += [
            f"\n### {p['name']}",
            f"\n- Problem: {p['problem']}",
            f"- Objective: {p['objective']}",
            f"- Skills: {', '.join(p['skills'])}",
            f"- Minimum scope: {p['scope']}",
            f"- Evidence: {p['evidence']}",
            f"- Before listing: {p['before_listing']}",
        ]
    if not a.projects:
        lines.append("\nNo skill gap was detected to ground a project idea in.")
    lines += [
        "\n## Limitations",
        "\nDictionary matching is English-only and incomplete. TF-IDF measures word overlap and can miss equivalent meanings. Job requirement grouping is a heuristic; review the detected skills and correct the job text before relying on the result.",
    ]
    return "\n".join(lines)

