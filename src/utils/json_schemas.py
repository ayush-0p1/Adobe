# src/utils/json_schemas.py
ROUND_1A_SCHEMA = {
    "type": "object",
    "properties": {
        "document_title": {"type": "string"},
        "extraction_timestamp": {"type": "string"},
        "outline": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "level": {"type": "string", "enum": ["H1", "H2", "H3"]},
                    "title": {"type": "string"},
                    "page_number": {"type": "integer"},
                    "section_id": {"type": "string"}
                },
                "required": ["level", "title", "page_number"]
            }
        },
        "metadata": {
            "type": "object",
            "properties": {
                "total_pages": {"type": "integer"},
                "processing_time_seconds": {"type": "number"},
                "language": {"type": "string"}
            }
        }
    },
    "required": ["document_title", "extraction_timestamp", "outline"]
}
