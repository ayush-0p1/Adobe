import json
from pathlib import Path
from .intelligence_engine import IntelligenceEngine
from .persona_analyzer import PersonaAnalyzer

INPUT_DIR = Path('/app/input')
OUTPUT_DIR = Path('/app/output') / 'round1b_output.json'


def main():
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
    engine.process(pdfs, persona, job, OUTPUT_DIR)

if __name__ == '__main__':
    main()
    