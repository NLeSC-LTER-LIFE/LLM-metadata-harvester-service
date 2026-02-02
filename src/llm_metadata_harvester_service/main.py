from fastapi import FastAPI
from llm_metadata_harvester_service.api.jobs import router as jobs_router

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="LLM metadata harvester Service")

app.include_router(jobs_router, prefix="/jobs")

@app.get("/health")
async def health():
    return {"status": "ok"}
