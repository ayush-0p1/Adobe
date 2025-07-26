import json
import os
import logging
from pathlib import Path
from .outline_extractor import OutlineExtractor
from ..utils.performance_monitor import PerformanceMonitor

INPUT_DIR = Path('/app/input')
OUTPUT_DIR = Path('/app/output')
MAX_EXEC_TIME = float(os.getenv('MAX_EXEC_TIME', '30'))
MAX_MEMORY_MB = float(os.getenv('MAX_MEMORY_MB', '500'))


def process_all_pdfs():
    logging.basicConfig(level=logging.INFO)
    extractor = OutlineExtractor()
    monitor = PerformanceMonitor()
    for pdf_file in INPUT_DIR.glob('*.pdf'):
        with monitor.measure_execution(f'extract_{pdf_file.name}'):
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
    monitor.check_constraints(MAX_EXEC_TIME, MAX_MEMORY_MB)

if __name__ == '__main__':
    process_all_pdfs()
    