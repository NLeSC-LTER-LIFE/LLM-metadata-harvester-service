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
