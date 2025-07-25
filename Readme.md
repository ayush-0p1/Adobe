# PDF Outline Extractor

This repository contains a reference solution for the Adobe "Connecting the
Dots" challenge. The project demonstrates how to extract structured outlines
from PDF files (Round 1A) and provides a lightweight framework for persona
driven analysis (Round 1B).

## Building the Docker Image

```bash
docker build --platform linux/amd64 -t outline_extractor:latest .
```

## Running

Place PDF documents in an `input` directory and mount it along with an
`output` directory when running the container:

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none outline_extractor:latest
```

JSON outlines will be produced in the output directory with the same base name
as each PDF. The generated JSON conforms to the schema provided in the official
sample dataset repository.