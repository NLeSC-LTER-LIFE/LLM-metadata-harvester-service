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
):
    """
    Submit a metadata harvesting job.
    """
    task = run_harvester_task.delay(
        model=payload.model,
        url=payload.url,
        api_key=x_api_key,
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







"""
from fastapi import APIRouter
from celery.result import AsyncResult
from llm_metadata_harvester_service.api.schemas import JobRequest, JobStatusResponse
from llm_metadata_harvester_service.workers.tasks import run_harvester_task
from llm_metadata_harvester_service.core.celery_app import celery_app

router = APIRouter()

@router.post("/", response_model=JobStatusResponse)
async def submit_job(req: JobRequest):
    task = run_harvester_task.delay(
        model=req.model,
        api_key=req.api_key.get_secret_value(),
        url=req.url,
    )
    return JobStatusResponse(job_id=task.id, status="queued")

@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    result = AsyncResult(job_id, app=celery_app)

    if result.state =="PENDING":
        return JobStatusResponse(job_id=job_id, status="pending")
    
    if result.state == "FAILURE":
        return JobStatusResponse(
            job_id=job_id,
            status="failed",
            error=str(result.result),
        )

    if result.state == "SUCCESS":
        return JobStatusResponse(
            job_id=job_id,
            status="success",
            result=result.result,
        )

    #response = {
    #    "job_id": job_id,
    #    "status": result.state,
    #    "result": None,
    #    "error": None,
    #}

    #if result.successful():
    #    response["result"] = result.result
    #elif result.failed():
    #    response["error"] = str(result.result)

    #return response

    return JobStatusResponse(job_id=job_id, status=result.state)

@router.get("/{job_id}/result")
async def get_job_result(job_id: str):
    result = AsyncResult(job_id, app=celery_app)

    if not result.ready():
        return {"status": result.state}

    if result.failed():
        raise HTTPException(status_code=500, detail=str(result.result))

    return {"status": "SUCCESS", "result": result.result}
"""