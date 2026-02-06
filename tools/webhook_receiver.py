#!/usr/bin/env python3
import hmac
import hashlib
import os
from fastapi import FastAPI, Request, HTTPException
import uvicorn

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "test-secret")
HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")
PORT = int(os.getenv("WEBHOOK_PORT", "9000"))

app = FastAPI(title="Local Webhook Receiver")


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Webhook-Signature")

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    if signature != f"sha256={expected}":
        raise HTTPException(status_code=401, detail="Invalid signature")

    print("\n✅ Webhook received and verified")
    print(body.decode())
    return {"status": "ok"}


if __name__ == "__main__":
    print("🚀 Starting webhook receiver")
    print(f"   URL: http://{HOST}:{PORT}/webhook")
    print(f"   Secret: {WEBHOOK_SECRET}")

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info",
    )
