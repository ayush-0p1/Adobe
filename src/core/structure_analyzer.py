from collections import Counter
from typing import List
from .base_models import TextBlock, Heading, DocumentOutline
from datetime import datetime

class StructureAnalyzer:
    """Simple heuristics to determine heading levels based on font sizes."""

    def _determine_font_thresholds(self, text_blocks: List[TextBlock]):
        sizes = [tb.font_size for tb in text_blocks if tb.font_size > 0]
        if not sizes:
            # Fallback sizes when font information is unavailable
            return 1, 1, 1
        size_counts = Counter(sizes)
        common_sizes = [s for s, _ in size_counts.most_common()]
        base = common_sizes[-1] if len(common_sizes) > 0 else min(sizes)
        h3 = base
        h2 = max(size for size in sizes if size > h3) if any(size > h3 for size in sizes) else h3
        h1 = max(size for size in sizes if size > h2) if any(size > h2 for size in sizes) else h2
        return h1, h2, h3

    def detect_headings(self, text_blocks: List[TextBlock]) -> List[Heading]:
        headings: List[Heading] = []
        if not text_blocks:
            return headings
        h1_size, h2_size, h3_size = self._determine_font_thresholds(text_blocks)
        for i, block in enumerate(text_blocks):
            size = block.font_size
            level = None
            if h1_size == h2_size == h3_size == 1:
                if i == 0:
                    level = "H1"
                elif i == 1:
                    level = "H2"
                else:
                    level = "H3"
            else:
                if size >= h1_size:
                    level = "H1"
                elif size >= h2_size:
                    level = "H2"
                elif size >= h3_size:
                    level = "H3"
            if level:
                headings.append(
                    Heading(
                        level=level,
                        text=block.text,
                        page_number=block.page_number,
                    )
                )
        return headings

    def create_outline(self, text_blocks: List[TextBlock], title: str) -> DocumentOutline:
        headings = self.detect_headings(text_blocks)
        outline = DocumentOutline(
            title=title or "",
            outline=headings,
            extraction_timestamp=datetime.utcnow(),
        )
        return outline