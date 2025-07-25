# tests/test_basic_functionality.py
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
    assert outline.document_title is not None
    assert len(outline.outline) > 0

def test_json_output_format():
    # Test JSON schema compliance
    # Implementation here
    pass
