import json
import os
import logging
from pathlib import Path
from .intelligence_engine import IntelligenceEngine
from .persona_analyzer import PersonaAnalyzer
from ..utils.performance_monitor import PerformanceMonitor

INPUT_DIR = Path('/app/input')
OUTPUT_DIR = Path('/app/output') / 'round1b_output.json'
MAX_EXEC_TIME = float(os.getenv('MAX_EXEC_TIME', '30'))
MAX_MEMORY_MB = float(os.getenv('MAX_MEMORY_MB', '500'))


def main():
    logging.basicConfig(level=logging.INFO)
    monitor = PerformanceMonitor()
    pdfs = [str(p) for p in INPUT_DIR.glob('*.pdf')]
    persona_data = {
        'role': 'Researcher',
        'expertise_level': 'expert',
        'focus': 'AI'
    }
    job_data = {
        'task': 'Summarize key sections'
    }
    analyzer = PersonaAnalyzer()
    persona = analyzer.create_persona(persona_data)
    job = analyzer.create_job(job_data)
    engine = IntelligenceEngine()
    with monitor.measure_execution('round1b_process'):
        engine.process(pdfs, persona, job, OUTPUT_DIR)
    monitor.check_constraints(MAX_EXEC_TIME, MAX_MEMORY_MB)

if __name__ == '__main__':
    main()
    
