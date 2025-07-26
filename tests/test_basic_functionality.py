import os, sys
from pathlib import Path
sys.path.insert(0, os.path.abspath("."))
sys.path.append(os.path.abspath("src"))
import pytest
import json
import fitz
from src.core.pdf_processor import PDFProcessor
from src.round1a.outline_extractor import OutlineExtractor
from src.round1b.intelligence_engine import IntelligenceEngine
from src.round1b.persona_analyzer import PersonaAnalyzer

@pytest.fixture(scope="session", autouse=True)
def create_test_pdfs():
    base = Path("tests/test_pdfs")
    base.mkdir(parents=True, exist_ok=True)

    simple = base / "simple.pdf"
    if not simple.exists():
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Title", fontsize=20)
        page.insert_text((72, 100), "Section 1", fontsize=16)
        page.insert_text((72, 120), "Content", fontsize=12)
        doc.save(simple)
        doc.close()

    structured = base / "structured.pdf"
    if not structured.exists():
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Structured Document", fontsize=20)
        page.insert_text((72, 100), "Heading One", fontsize=16)
        page.insert_text((72, 120), "Text under heading", fontsize=12)
        page.insert_text((72, 150), "Heading Two", fontsize=16)
        page.insert_text((72, 170), "More text", fontsize=12)
        doc.save(structured)
        doc.close()
    return str(base)

def test_pdf_processing():
    processor = PDFProcessor()
    # Test with a simple PDF
    text_blocks = processor.extract_text_with_metadata("tests/test_pdfs/simple.pdf")
    assert len(text_blocks) > 0

def test_outline_extraction():
    extractor = OutlineExtractor()
    outline = extractor.extract_outline("tests/test_pdfs/structured.pdf")
    assert outline.title is not None
    assert len(outline.outline) > 0

def test_json_output_format():
    extractor = OutlineExtractor()
    outline = extractor.extract_outline("tests/test_pdfs/simple.pdf")
    output = {
        "title": outline.title,
        "outline": [
            {"level": h.level, "text": h.text, "page": h.page_number}
            for h in outline.outline
        ],
    }
    assert "title" in output
    assert isinstance(output["outline"], list)
    for item in output["outline"]:
        assert set(item.keys()) == {"level", "text", "page"}


def test_intelligence_engine_process(tmp_path):
    engine = IntelligenceEngine()
    analyzer = PersonaAnalyzer()
    persona = analyzer.create_persona({"role": "Researcher", "expertise_level": "expert", "focus": "AI"})
    job = analyzer.create_job({"task": "Summarize"})
    out_file = tmp_path / "output.json"
    engine.process([
        "tests/test_pdfs/simple.pdf",
        "tests/test_pdfs/structured.pdf",
    ], persona, job, out_file)
    with open(out_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert set(data.keys()) == {"metadata", "extracted_sections", "sub_section_analysis"}
    assert "processing_timestamp" in data["metadata"]
    assert isinstance(data["metadata"]["ranked_documents"], list)
    assert isinstance(data["extracted_sections"], dict)
    first_doc = "tests/test_pdfs/simple.pdf"
    assert first_doc in data["extracted_sections"]
    if data["extracted_sections"][first_doc]:
        assert "importance" in data["extracted_sections"][first_doc][0]