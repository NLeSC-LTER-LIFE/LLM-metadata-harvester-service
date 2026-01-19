import subprocess
import tempfile
import json
import os

METADATA_HARVESTER_IMAGE = "/opt/containers/llm-metadata-harvester-service.sif"

def run_apptainer(model: str, api_key: str, input_text: str):

    args = [
        "--api-key", api-key,
        "--model-name", model_name,
        "--url", url,
    ]

    env = {}
    env["APPTAINERENV_ENTRYPOINT_ARGS"] = "\n".join(args)

    cmd = [
        "apptainer", "run",
        "--cleanenv",
        "--containall",
        "--no-home",
        METADATA_HARVESTER_IMAGE,
        
    ]

    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout

