FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy source code
COPY src/ ./src/
COPY models/ ./models/

# Create input/output directories
RUN mkdir -p /app/input /app/output

# Set environment variables
ENV PYTHONPATH=/app/src
ENV TOKENIZERS_PARALLELISM=false

# Entry point for Round 1A
CMD ["python", "src/round1a/main.py"]
