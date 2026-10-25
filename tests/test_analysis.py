import pytest
from careerlens.analysis import analyze
from careerlens.report import markdown
from careerlens.skills import detect_skills
from careerlens.extraction import extract_upload, normalize


def test_aliases_and_boundaries():
    found = detect_skills("Used sklearn and NLP. The word pythonesque is unrelated.", "resume")
    assert {s.name for s in found} == {"scikit-learn", "NLP"}


def test_duplicate_mentions_count_once():
    a = analyze("Python Python Python", "Required skills:\nPython")
    assert a.required_coverage == 100


def test_gaps_and_evidence():
    a = analyze("Built a model with Python", "Required skills:\nPython\nPyTorch")
    assert a.gaps == ["PyTorch"]
    assert "Python" in a.matches[0].evidence
    assert a.projects and "PyTorch" in a.projects[0]["skills"]


def test_zero_vector_and_score_range():
    a = analyze("unmatchedword", "required\nPyTorch")
    assert a.text_similarity == 0
    assert 0 <= a.score <= 100


def test_empty_inputs():
    with pytest.raises(ValueError):
        analyze("", "job")


def test_extraction_and_report():
    assert extract_upload("resume.txt", b"Python\r\n\r\nSQL") == "Python\n\nSQL"
    with pytest.raises(ValueError):
        extract_upload("resume.exe", b"x")
    a = analyze("Python", "Required\nPython")
    assert "alignment" in markdown(a)


def test_normalize():
    assert normalize("A   B\n\n\nC") == "A B\n\nC"


def test_pdf_extraction_and_image_only_error():
    import fitz

    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "Python and SQL")
    data = pdf.tobytes()
    pdf.close()
    assert "Python and SQL" in extract_upload("resume.pdf", data)

    empty = fitz.open()
    empty.new_page()
    with pytest.raises(ValueError, match="image-only scan"):
        extract_upload("scan.pdf", empty.tobytes())
    empty.close()


def test_docx_extraction():
    from docx import Document
    from io import BytesIO

    document = Document()
    document.add_paragraph("Built a Python service")
    buffer = BytesIO()
    document.save(buffer)
    assert extract_upload("resume.docx", buffer.getvalue()) == "Built a Python service"


def test_size_limit_and_corrupt_pdf():
    with pytest.raises(ValueError, match="10 MB"):
        extract_upload("resume.txt", b"x" * (10 * 1024 * 1024 + 1))
    with pytest.raises(Exception):
        extract_upload("broken.pdf", b"not a pdf")

