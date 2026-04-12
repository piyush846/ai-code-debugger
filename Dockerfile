FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e . && pip install --no-cache-dir requests

ENV AIDBG_MODEL=qwen2.5-coder:1.5b
ENV AIDBG_OLLAMA_HOST=http://ollama:11434
ENV AIDBG_MAX_ATTEMPTS=4
ENV AIDBG_TIMEOUT=600

CMD ["python", "-m", "aidbg.cli", "--help"]