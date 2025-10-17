from fastapi import FastAPI
from pydantic import BaseModel
import os
import subprocess

app = FastAPI(title="TSRTC Tracking API")

class TrackRequest(BaseModel):
    consignment: str

@app.post("/track")
def track_package(req: TrackRequest):

    env_vars = {**os.environ, "CONS_NUMBER": req.consignment}

    result = subprocess.run(
        ["python", "lr.py"],
        env=env_vars,
        capture_output=True,
        text=True
    )

    stdout_output = result.stdout.strip().split("\n") if result.stdout else ["No output received."]
    stderr_output = result.stderr.strip().split("\n") if result.stderr else []

    response = {
        "tracking": stdout_output,
        "errors": stderr_output,
        "returncode": result.returncode
    }

    return response

@app.get("/health")
def health_check():
    return {"status": "ok"}
