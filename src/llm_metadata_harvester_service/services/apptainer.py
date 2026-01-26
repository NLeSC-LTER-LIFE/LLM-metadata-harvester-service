import subprocess
from dataclasses import dataclass
from typing import Optional
import tempfile
import json
import os

METADATA_HARVESTER_IMAGE = "/opt/containers/llm-metadata-harvester-service.sif"

@dataclass
class ApptainerResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0

def run_apptainer(
        model: str, 
        api_key: str, 
        url: str, 
        timeout: int=600
) -> ApptainerResult:

    args = [
        "--api-key", api_key,
        "--model-name", model,
        "--url", url,
    ]

    env = {}
    env["APPTAINERENV_ENTRYPOINT_ARGS"] = " ".join(args)

    cmd = [
        "apptainer", 
        "run",
        "--cleanenv",
        "--containall",
        "--no-home",
        METADATA_HARVESTER_IMAGE,
        
    ]

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )

        return ApptainerResult(
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    
    except subprocess.TimeoutExpired as e:
        return ApptainerResult(
            returncode=-1,
            stdout=e.stdout or "",
            stderr="Execution timed out",
            timed_out=True,
        )

