ROUND_1A_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "outline": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "level": {"type": "string", "enum": ["H1", "H2", "H3"]},
                    "text": {"type": "string"},
                    "page": {"type": "integer"}
                },
                "required": ["level", "text", "page"]
            }
        }
    },
    "required": ["title", "outline"]
}
