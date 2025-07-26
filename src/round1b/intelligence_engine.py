import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from ..core.pdf_processor import PDFProcessor
from ..core.structure_analyzer import StructureAnalyzer
from ..core.base_models import Persona, JobToBeDone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class IntelligenceEngine:
    def __init__(self):
        self.processor = PDFProcessor()
        self.analyzer = StructureAnalyzer()
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def _aggregate_text(self, pdfs: List[str]) -> List[str]:
        texts = []
        for pdf in pdfs:
            blocks = self.processor.extract_text_with_metadata(pdf)
            texts.append(" ".join(tb.text for tb in blocks))
        return texts

    def rank_documents(self, pdfs: List[str], persona: Persona, job: JobToBeDone) -> List[int]:
        docs_text = self._aggregate_text(pdfs)
        query = persona.role + " " + job.task_description
        tfidf = self.vectorizer.fit_transform(docs_text + [query])
        sims = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()
        ranked_indices = sims.argsort()[::-1]
        return ranked_indices.tolist()

    def _rank_sections(self, sections: List[str], query: str) -> List[float]:
        """Return similarity scores for a list of section texts."""
        if not sections:
            return []
        tfidf = self.vectorizer.fit_transform(sections + [query])
        sims = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()
        return sims.tolist()

    def process(self, pdfs: List[str], persona: Persona, job: JobToBeDone, output_path: Path):
        """Run the round1b pipeline and emit extended JSON output."""
        ranked = self.rank_documents(pdfs, persona, job)
        query = persona.role + " " + job.task_description

        extracted_sections: Dict[str, List[Dict]] = {}
        sub_section_analysis: Dict[str, List[Dict]] = {}

        for pdf in pdfs:
            blocks = self.processor.extract_text_with_metadata(pdf)
            headings = self.analyzer.detect_headings(blocks)
            section_texts = [h.text for h in headings]
            scores = self._rank_sections(section_texts, query)
            ranked_sections = [
                {
                    'level': h.level,
                    'text': h.text,
                    'page': h.page_number,
                    'importance': scores[i] if i < len(scores) else 0.0,
                }
                for i, h in enumerate(headings)
            ]
            ranked_sections.sort(key=lambda x: x['importance'], reverse=True)
            extracted_sections[pdf] = ranked_sections

            sub_section_analysis[pdf] = [
                {
                    'heading': h.text,
                    'analysis': f"length:{len(h.text.split())}",
                }
                for h in headings
            ]

        output = {
            'metadata': {
                'documents': pdfs,
                'persona': persona.__dict__,
                'job': job.__dict__,
                'processing_timestamp': datetime.utcnow().isoformat(),
                'ranked_documents': ranked,
            },
            'extracted_sections': extracted_sections,
            'sub_section_analysis': sub_section_analysis,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)