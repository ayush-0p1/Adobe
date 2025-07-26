import pdfplumber
from .base_models import TextBlock
from typing import List

class PDFProcessor:
    """Extract text blocks with basic font metadata using pdfplumber."""

    def extract_text_with_metadata(self, pdf_path: str) -> List[TextBlock]:
        text_blocks: List[TextBlock] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                try:
                    words = page.extract_words(
                        use_text_flow=True,
                        keep_blank_chars=False,
                        extra_attrs=["fontname", "size"],
                    )
                except Exception:
                    # fallback simple extraction
                    words = []
                for w in words:
                    text = w.get("text", "").strip()
                    if not text:
                        continue
                    # pdfplumber provides fontname and size if extracted with chars
                    font_size = float(w.get("size", 0))
                    font_name = w.get("fontname", "")
                    bbox = (w.get("x0", 0), w.get("top", 0), w.get("x1", 0), w.get("bottom", 0))
                    text_blocks.append(
                        TextBlock(
                            text=text,
                            page_number=page_number,
                            bbox=bbox,
                            font_size=font_size,
                            font_name=font_name,
                            is_bold="Bold" in font_name,
                            is_italic="Italic" in font_name,
                        )
                    )
        return text_blocks
    