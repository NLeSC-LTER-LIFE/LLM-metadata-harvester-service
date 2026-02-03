FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ---- install llm-metadata-harvester from source ----
WORKDIR /opt

RUN git clone https://github.com/LTER-LIFE/llm-metadata-harvester.git \
    && cd llm-metadata-harvester \
    && pip install --no-cache-dir .

RUN playwright install-deps \ 
    && playwright install chromium chromium-headless-shell

WORKDIR /app

# Copy source code
COPY pyproject.toml .
COPY src/llm_metadata_harvester_service ./src/llm_metadata_harvester_service

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["gunicorn", "src.llm_metadata_harvester_service.main:app", "-c", "src/llm_metadata_harvester_service/gunicorn_conf.py"]
