# src/llm_metadata_harvester_service/workers/tasks.py

from celery import shared_task
import io
import sys
import json
import traceback
import asyncio
from contextlib import redirect_stdout
import os
import requests
import hmac
import hashlib
import time

from llm_metadata_harvester.harvester_operations import metadata_harvest


@shared_task(bind=True)
def run_harvester_task(self, *, model: str, url: str, api_key: str, callback_url: str | None = None, webhook_secret: str | None = None):
    stdout_buffer = io.StringIO()

    try:
        with redirect_stdout(stdout_buffer):
            result = asyncio.run(
                metadata_harvest(
                    model_name=model,
                    url=url,
                    api_key=api_key,
                )
            )

        logs = stdout_buffer.getvalue()

        payload = {
            "model": model,
            "result": result,
            "logs": logs,
        }

        if callback_url:
            send_webhook(callback_url, webhook_secret, self.request.id, payload)

        # Operator visibility (optional)
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        sys.stdout.flush()

        return payload

    except Exception:
        error_logs = stdout_buffer.getvalue() + "\n" + traceback.format_exc()

        payload = {
            "model": model,
            "result": None,
            "logs": error_logs,
            "error": "harvest_failed",
        }

        sys.stderr.write(json.dumps(payload) + "\n")
        sys.stderr.flush()

        raise

def send_webhook(callback_url: str, webhook_secret: str, job_id: str, payload: dict):
    body = {
        "job_id": job_id,
        "status": "success",
        "timestamp": int(time.time()),
    }

    headers = {"Content-Type":"application/son"}
    signature = sign_webhook(body, webhook_secret)
    headers["X-Signature"] = signature

    try:
        requests.post(
            callback_url,
            json=body,
            headers=headers,
            timeout=10,
        )
    except Exception:
        #log but don't fail job. Best effort only
        traceback.print_exc()

def sign_webhook(wh_body: dict, secret: str) -> str:
    return hmac.new(
        secret.endcode(),
        json.dumps(wh_body, separators=(",", ":")).encode(),
        hashlib.sha256
    ).hexdigest()
