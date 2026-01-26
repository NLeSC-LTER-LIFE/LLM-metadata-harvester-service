from pydantic import BaseModel, SecretStr
from typing import Optional, Any

class JobRequest(BaseModel):
    job_id: str
    api_key: SecretStr
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "model": "gemini-2.5-flash",
                "api_key": "sk-...",
                "url": "https://example.com"
            }
        }    


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
