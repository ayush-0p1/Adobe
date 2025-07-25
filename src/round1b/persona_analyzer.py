from dataclasses import dataclass
from typing import Dict
from ..core.base_models import Persona, JobToBeDone

@dataclass
class PersonaDefinition:
    role: str
    expertise_level: str
    focus: str

class PersonaAnalyzer:
    def create_persona(self, data: Dict) -> Persona:
        return Persona(
            role=data.get('role', ''),
            expertise_level=data.get('expertise_level', ''),
            primary_interests=[data.get('focus', '')],
            context='' ,
        )

    def create_job(self, data: Dict) -> JobToBeDone:
        return JobToBeDone(
            task_description=data.get('task', ''),
            expected_output='',
            success_criteria=[],
            constraints=[],
        )