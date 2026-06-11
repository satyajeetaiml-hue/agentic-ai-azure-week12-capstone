"""Week 12 — Capstone: Build, Demo & Review.

Customer Onboarding Automation: a multi-agent staged pipeline (intake -> KYC ->
risk -> provisioning). Run:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.service import CapstoneRequest, CapstoneResponse, get_settings, run_pipeline

settings = get_settings()
app = FastAPI(title="Week 12 — Capstone (Customer Onboarding)", version="0.2.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok", "week": "12", "backend": "foundry" if settings.use_foundry else "mock"}


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": "agentic-ai-azure-week12-capstone",
        "endpoint": "/api/v1/capstone",
        "backend": "foundry" if settings.use_foundry else "mock",
        "docs": "/docs",
    }


@app.post("/api/v1/capstone", response_model=CapstoneResponse, tags=["week12"])
def capstone(payload: CapstoneRequest) -> CapstoneResponse:
    return run_pipeline(payload)
