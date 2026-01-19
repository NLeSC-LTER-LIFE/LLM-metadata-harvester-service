from fastapi import FastAPI
from llm-metadata-harvester-service.api.jobs import router as jobs_router

app = FastAPI(title="LLM metadata harvester Service")

app.include_router(jobs_router, prefix="/jobs")
