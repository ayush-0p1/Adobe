# Approach Explanation

This repository contains a minimal reference implementation for the "Connecting the Dots" challenge. The goal of Round 1A is to extract a structured outline (title and headings) from PDF documents. Round 1B extends this by ranking and extracting relevant sections for a specific persona and job to be done.

## Round 1A

The solution uses **pdfplumber** to read each PDF page and extract individual words along with their font size and font name. These word tokens are grouped into `TextBlock` dataclasses that capture their location, font attributes and page number. A `StructureAnalyzer` then performs simple heuristics to assign heading levels based on the relative font sizes found in the document. The largest recurring font size is treated as H1, the next largest as H2 and so on. Detected headings are returned as `Heading` dataclasses and assembled into a `DocumentOutline`. The `main.py` script iterates over all PDFs in `/app/input` and writes a JSON outline for each file to `/app/output`. The JSON matches the schema published in the sample challenge repository, with the keys `title`, `outline[level,text,page]`.

## Round 1B

Round 1B introduces a lightweight `IntelligenceEngine` which relies on TF‑IDF vectors from scikit‑learn to rank documents for a given persona and job query. Text is aggregated from each PDF using the same `PDFProcessor`. The engine then computes cosine similarity between the query and each document to produce a ranked list. A `PersonaAnalyzer` converts simple dictionaries into `Persona` and `JobToBeDone` models. The final output is written as a JSON file in the output directory.

This implementation is intentionally small and self‑contained so it can run within the provided docker environment without network access. It does not use any large pretrained models; all processing is performed with built‑in Python libraries and scikit‑learn. The container entry point defaults to the Round 1A pipeline.
