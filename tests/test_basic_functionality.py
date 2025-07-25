import os, sys
sys.path.insert(0, os.path.abspath("."))
sys.path.append(os.path.abspath("src"))
import pytest
import json
from src.core.pdf_processor import PDFProcessor
from src.round1a.outline_extractor import OutlineExtractor

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