FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src ./src

RUN pip install --no-cache-dir .

# Apptainer binary must exist on host or be mounted
# We assume /usr/bin/apptainer is available at runtime

EXPOSE 8000

CMD ["gunicorn", "src.llm_metadata_harvester_service.main:app", "-c", "src/llm_metadata_harvester_service/gunicorn_conf.py"]
