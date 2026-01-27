import subprocess
from dataclasses import dataclass
from typing import Optional
import tempfile
import json
import os
import inspect

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

    print("RUNN_APPTAINER FROM:", inspect.getfile(run_apptainer))
    print("CHECK_TRUE_PRESENT:", "check=True" in inspect.getsource(run_apptainer))
    import llm_metadata_harvester_service.services.apptainer as a
    print(a.__file__) 

    args = [
        "--api-key", api_key,
        "--model-name", model,
        "--url", url,
    ]

    #env = {}
    env = os.environ.copy()
    env["APPTAINERENV_ENTRYPOINT_ARGS"] = " ".join(args)
    print(env)

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

