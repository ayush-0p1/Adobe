from typing import List
from ..core.pdf_processor import PDFProcessor
from ..core.structure_analyzer import StructureAnalyzer
from ..core.base_models import DocumentOutline

class OutlineExtractor:
    def __init__(self):
        self.processor = PDFProcessor()
        self.analyzer = StructureAnalyzer()

    def extract_outline(self, pdf_path: str) -> DocumentOutline:
        text_blocks = self.processor.extract_text_with_metadata(pdf_path)
        title = text_blocks[0].text if text_blocks else ""
        return self.analyzer.create_outline(text_blocks, title)