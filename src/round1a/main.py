import json
import os
from pathlib import Path
from .outline_extractor import OutlineExtractor

INPUT_DIR = Path('/app/input')
OUTPUT_DIR = Path('/app/output')


def process_all_pdfs():
    extractor = OutlineExtractor()
    for pdf_file in INPUT_DIR.glob('*.pdf'):
        outline = extractor.extract_outline(str(pdf_file))
        output = {
            'title': outline.title,
            'outline': [
                {
                    'level': h.level,
                    'text': h.text,
                    'page': h.page_number,
                }
                for h in outline.outline
            ],
        }
        out_path = OUTPUT_DIR / f"{pdf_file.stem}.json"
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    process_all_pdfs()