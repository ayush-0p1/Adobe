# src/core/base_models.py
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class TextBlock:
    text: str
    page_number: int
    bbox: tuple  # (x0, y0, x1, y1)
    font_size: float
    font_name: str
    is_bold: bool
    is_italic: bool

@dataclass
class Heading:
    level: str  # H1, H2, H3
    text : str
    page_number: int

@dataclass
class DocumentOutline:
    title : str
    outline: List[Heading]
    extraction_timestamp: datetime

@dataclass
class Persona:
    role: str
    expertise_level: str
    primary_interests: List[str]
    context: str

@dataclass
class JobToBeDone:
    task_description: str
    expected_output: str
    success_criteria: List[str]
    constraints: List[str]
    
