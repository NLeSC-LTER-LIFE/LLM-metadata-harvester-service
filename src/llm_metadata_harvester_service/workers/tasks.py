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
                    model=model,
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


"""
from llm_metadata_harvester_service.core.celery_app import celery_app
from llm_metadata_harvester_service.services.apptainer import run_apptainer, ApptainerResult
from celery import shared_task
from typing import Optional
import subprocess
import json

@celery_app.task(bind=True)
def run_harvester_task(self, model: str, api_key: str, url: str):
    self.update_state(state="STARTED")
    result = run_apptainer(
        model=model,
        api_key=api_key,
        url=url,
    )

    if not result.ok:
        raise RuntimeError(
            f"Apptainer failed (rc={result.returncode})\n{result.stderr}"
        )

    if result.timed_out:
        raise RuntimeError(result.stderr or 'Apptainer execution failed')
    
    # Parse structured JSON from stdout
    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "Container did not emit valid JSON on stdout"
        ) from e
    
    # Return normalized, API-ready object
    return {
        "model": model,
        "source_url": url,
        "metadata": parsed,
        "returncode": result.returncode,
        "stderr": result.stderr,
    }
    
    #return {
    #    "stdout": result.stdout,
    #    "stderr": result.stderr,
    #    "returncode": result.returncode
    #}

@shared_task(bind=True)
def apptainer_smoke_test(self):
    sif_path = "/opt/containers/llm-metadata-harvester-service.sif"

    cmd = [
        "apptainer",
        "exec",
        sif_path,
        "python",
        "--version",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )

    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
"""