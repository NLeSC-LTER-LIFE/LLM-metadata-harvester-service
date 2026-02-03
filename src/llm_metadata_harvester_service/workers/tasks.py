# src/llm_metadata_harvester_service/workers/tasks.py

from celery import shared_task
import io
import sys
import json
import traceback
import asyncio
from contextlib import redirect_stdout

from llm_metadata_harvester.harvester_operations import metadata_harvest


@shared_task(bind=True)
def run_harvester_task(self, *, model: str, url: str, api_key: str):
    stdout_buffer = io.StringIO()

    try:
        with redirect_stdout(stdout_buffer):
            result = asyncio.run(
                metadata_harvest(
                    model_name=model,
                    url=url,
                    api_key=api_key,
                )
            )

        logs = stdout_buffer.getvalue()

        payload = {
            "model": model,
            "result": result,
            "logs": logs,
        }

        # Operator visibility (optional)
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        sys.stdout.flush()

        return payload

    except Exception:
        error_logs = stdout_buffer.getvalue() + "\n" + traceback.format_exc()

        payload = {
            "model": model,
            "result": None,
            "logs": error_logs,
            "error": "harvest_failed",
        }

        sys.stderr.write(json.dumps(payload) + "\n")
        sys.stderr.flush()

        raise
