from llm-metadata-harvester.core.celery_app import celery_app
from llm-metadata-harvester.services.apptainer import run_apptainer

@celery_app.task(bind=True)
def run_harvester_task(self, model: str, api_key: str, url: str):
    self.update_state(state="STARTED")
    return run_apptainer(
        model=model,
        api_key=api_key,
        url=url,
    )
