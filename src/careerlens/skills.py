"""Small, transparent English-language skill dictionary."""

import re
from dataclasses import dataclass

SKILLS = {
    "Python": ("Programming languages", ["python"]),
    "Java": ("Programming languages", ["java"]),
    "JavaScript": ("Programming languages", ["javascript", "js"]),
    "SQL": ("Programming languages", ["sql"]),
    "C++": ("Programming languages", ["c++"]),
    "Machine learning": ("Machine learning", ["machine learning", "ml"]),
    "scikit-learn": ("Machine learning", ["scikit-learn", "sklearn"]),
    "TensorFlow": ("Machine learning", ["tensorflow"]),
    "PyTorch": ("Machine learning", ["pytorch"]),
    "NLP": ("NLP and generative AI", ["nlp", "natural language processing"]),
    "LLM": ("NLP and generative AI", ["llm", "large language model", "large language models"]),
    "Generative AI": ("NLP and generative AI", ["generative ai"]),
    "pandas": ("Frameworks and libraries", ["pandas"]),
    "NumPy": ("Frameworks and libraries", ["numpy"]),
    "FastAPI": ("Frameworks and libraries", ["fastapi"]),
    "Streamlit": ("Frameworks and libraries", ["streamlit"]),
    "Flask": ("Frameworks and libraries", ["flask"]),
    "PostgreSQL": ("Databases", ["postgresql", "postgres"]),
    "MySQL": ("Databases", ["mysql"]),
    "MongoDB": ("Databases", ["mongodb"]),
    "AWS": ("Cloud and deployment", ["aws", "amazon web services"]),
    "Docker": ("Cloud and deployment", ["docker"]),
    "Git": ("Developer tools", ["git"]),
    "Linux": ("Developer tools", ["linux"]),
    "REST API": ("Software engineering", ["rest api", "restful api"]),
    "Unit testing": ("Testing and software engineering", ["unit testing", "pytest", "unit tests"]),
}


@dataclass(frozen=True)
class Detection:
    name: str
    category: str
    evidence: str
    source: str
    requires_review: bool = False


def detect_skills(text: str, source: str) -> list[Detection]:
    found = []
    for name, (category, aliases) in SKILLS.items():
        for alias in aliases:
            pattern = re.compile(r"(?<![\w])" + re.escape(alias) + r"(?![\w])", re.I)
            match = pattern.search(text)
            if match:
                start, end = match.span()
                left, right = max(0, start - 65), min(len(text), end + 65)
                found.append(Detection(name, category, " ".join(text[left:right].split()), source))
                break
    return found

