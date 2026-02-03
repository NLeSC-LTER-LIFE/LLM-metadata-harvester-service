from pydantic import BaseModel, Field
from typing import Any, Dict, Optional



# Job submission
#=================

class JobSubmitRequest(BaseModel):
    model: str = Field(..., example="gemini-2.5-flash")
    url: str = Field(
        ...,
        example="https://example.com or doi:10.5281/zenodo.12345",
        description="URL, DOI, or other resolvable identifier",
    )


class JobSubmitResponse(BaseModel):
    job_id: str
    status: str



# Job status
# ===============

class JobStatusResponse(BaseModel):
    job_id: str
    status: str



# Job result
# =================

class JobResultResponse(BaseModel):
    job_id: str
    status: str
    model: str
    result: Dict[str, Any]
    logs: str
