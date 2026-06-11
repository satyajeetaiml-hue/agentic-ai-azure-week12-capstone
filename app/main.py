"""Week 12 — Capstone: Build, Demo & Review — starter FastAPI service.

Use case: Capstone Project (Pick one scenario).
See README.md for the full lab brief. Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Week 12 — Capstone: Build, Demo & Review", version="0.1.0")


class LabRequest(BaseModel):
    scenario: str = Field(..., min_length=1, description="The capstone scenario you are building.")


@app.get("/health")
def health():
    return {"status": "ok", "week": "12", "use_case": "Capstone Project"}


@app.get("/")
def root():
    return {
        "service": "agentic-ai-azure-week12-capstone",
        "week": "12",
        "endpoint": "/api/v1/capstone",
        "docs": "/docs",
    }


@app.post("/api/v1/capstone")
def handler(payload: LabRequest):
    """Mock handler for the Capstone Project.

    TODO (lab): replace this stub with the real implementation described in
    README.md (the Azure services for this week are listed in the Tech Stack).
    """
    return {
        "week": "12",
        "use_case": "Capstone Project",
        "received": payload.scenario,
        "status": "accepted",
        "note": "Mock response — implement the real agent per README.md.",
    }
