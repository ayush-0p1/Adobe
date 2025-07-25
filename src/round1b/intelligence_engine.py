import json
from pathlib import Path
from typing import List, Dict
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

    def process(self, pdfs: List[str], persona: Persona, job: JobToBeDone, output_path: Path):
        ranked = self.rank_documents(pdfs, persona, job)
        output = {
            'documents': pdfs,
            'persona': persona.__dict__,
            'job': job.__dict__,
            'processing_timestamp': 'N/A',
            'ranked_documents': ranked,
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)