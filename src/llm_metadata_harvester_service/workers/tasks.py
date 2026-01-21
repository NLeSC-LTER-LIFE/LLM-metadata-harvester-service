from llm_metadata_harvester_service.core.celery_app import celery_app
from llm_metadata_harvester_service.services.apptainer import run_apptainer
from celery import shared_task
import subprocess

@celery_app.task(bind=True)
def run_harvester_task(self, model: str, api_key: str, url: str):
    self.update_state(state="STARTED")
    return run_apptainer(
        model=model,
        api_key=api_key,
        url=url,
    )

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
