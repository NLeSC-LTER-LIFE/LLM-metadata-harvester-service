from fastapi import APIRouter, Depends, Header, HTTPException, status
from celery.result import AsyncResult

from llm_metadata_harvester_service.workers.tasks import run_harvester_task
from llm_metadata_harvester_service.core.celery_app import celery_app
from llm_metadata_harvester_service.api.schemas import (
    JobSubmitRequest,
    JobSubmitResponse,
    JobStatusResponse,
    JobResultResponse,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post(
    "/",
    response_model=JobSubmitResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit_job(
    payload: JobSubmitRequest,
    x_api_key: str = Header(..., alias="X-API-Key"),
    x_webhook_secret: Optional[str] = Header(
        None, alias="X-Webhook-Secret"
    ),
):
    """
    prevent insecure webhook registration
    """
    if payload.callback_url and not x_webhook_secret:
        raise HTTPEception(
            status_code=400,
            detal="X-Webhook-Secret required when callback_url is provided",
        )

    """
    Submit a metadata harvesting job.
    """
    task = run_harvester_task.delay(
        model=payload.model,
        url=payload.url,
        api_key=x_api_key,
        callback_url= payload.callback_url,
        webhook_secret=x_webhook_secret,
    )

    return JobSubmitResponse(
        job_id=task.id,
        status="queued",
    )


@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
)
async def get_job_status(job_id: str):
    """
    Lightweight status endpoint (no payload).
    """
    result = AsyncResult(job_id, app=celery_app)

    return JobStatusResponse(
        job_id=job_id,
        status=result.state.lower(),
    )


@router.get(
    "/{job_id}/result",
    response_model=JobResultResponse,
)
async def get_job_result(job_id: str):
    """
    Retrieve job result, logs, and model used.
    """
    result = AsyncResult(job_id, app=celery_app)

    if result.state == "PENDING":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Job still pending",
        )

    if result.state == "FAILURE":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(result.info),
        )

    if result.state != "SUCCESS":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Job in state: {result.state}",
        )

    payload = result.result

    return JobResultResponse(
        job_id=job_id,
        status="success",
        model=payload["model"],
        result=payload["result"],
        logs=payload["logs"],
    )
