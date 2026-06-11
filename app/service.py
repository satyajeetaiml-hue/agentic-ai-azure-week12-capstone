"""Week 12 — Capstone: Customer Onboarding Automation (multi-agent).

Brings the course together in one pipeline that mirrors patterns from earlier weeks:

* **Intake agent** (Wk1/2) — extract structured fields.
* **KYC/Compliance agent** (Wk6-7) — screening with a guardrail.
* **Risk agent** (Wk6-7) — score by requested amount.
* **Provisioning agent** (Wk5 tools) — create the account when cleared.

Runs as a sequential staged pipeline with per-stage status. Deterministic + offline;
``FOUNDRY_PROJECT_ENDPOINT`` toggles the reported mode. Other capstone scenarios
(transaction compliance, lead prioritization, document generation) follow the same shape.
"""

from __future__ import annotations

import re
import uuid
from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ── settings ────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    foundry_project_endpoint: str = ""
    foundry_model_name: str = "gpt-4o"
    review_amount_threshold: float = 100_000.0

    @property
    def use_foundry(self) -> bool:
        return bool(self.foundry_project_endpoint)


@lru_cache
def get_settings() -> Settings:
    return Settings()


# ── schemas ─────────────────────────────────────────────────────────────
class CapstoneRequest(BaseModel):
    scenario: str = Field(default="customer_onboarding", description="Capstone scenario id.")
    applicant_text: str = Field(..., min_length=1, description="Applicant / case details.")


class Stage(BaseModel):
    name: str
    status: str  # ok | flagged | skipped
    detail: str


class CapstoneResponse(BaseModel):
    scenario: str
    case_id: str
    decision: str  # onboarded | needs_review | rejected
    stages: list[Stage]
    extracted: dict
    mode: str


# ── agents (stages) ─────────────────────────────────────────────────────
def intake_stage(text: str) -> tuple[dict, Stage]:
    name = re.search(r"name[:\s]+([A-Za-z.\- ]+?)(?:,|$)", text, re.IGNORECASE)
    idn = re.search(r"\bID[-:\s]*([A-Z0-9]{4,})\b", text, re.IGNORECASE)
    amount_m = re.search(r"\$\s*([\d,]+)\s*(k)?", text)
    amount = None
    if amount_m:
        amount = float(amount_m.group(1).replace(",", "")) * (1000 if (amount_m.group(2) or "").lower() == "k" else 1)
    extracted = {
        "name": name.group(1).strip() if name else None,
        "id_number": idn.group(1).upper() if idn else None,
        "amount": amount,
    }
    return extracted, Stage(name="intake", status="ok", detail=f"Extracted {extracted}.")


def kyc_stage(text: str, extracted: dict) -> Stage:
    flagged = any(w in text.lower() for w in ("sanction", "watchlist", "pep"))
    if not extracted.get("id_number"):
        return Stage(name="kyc", status="flagged", detail="Missing ID number.")
    return Stage(
        name="kyc",
        status="flagged" if flagged else "ok",
        detail="Screening hit." if flagged else "KYC/AML clear.",
    )


def risk_stage(extracted: dict, threshold: float) -> Stage:
    amount = extracted.get("amount") or 0
    if amount > threshold:
        return Stage(name="risk", status="flagged", detail=f"High value (${amount:,.0f}) needs review.")
    return Stage(name="risk", status="ok", detail="Within auto-approve limit.")


def provisioning_stage(decision: str) -> Stage:
    if decision == "onboarded":
        return Stage(name="provisioning", status="ok", detail="Account provisioned.")
    return Stage(name="provisioning", status="skipped", detail=f"Not provisioned (decision={decision}).")


def run_pipeline(req: CapstoneRequest) -> CapstoneResponse:
    settings = get_settings()
    extracted, s_intake = intake_stage(req.applicant_text)
    s_kyc = kyc_stage(req.applicant_text, extracted)
    s_risk = risk_stage(extracted, settings.review_amount_threshold)

    if s_kyc.status == "flagged" and "hit" in s_kyc.detail.lower():
        decision = "rejected"
    elif s_kyc.status == "flagged" or s_risk.status == "flagged":
        decision = "needs_review"
    else:
        decision = "onboarded"

    s_prov = provisioning_stage(decision)
    return CapstoneResponse(
        scenario=req.scenario,
        case_id=f"CASE-{uuid.uuid4().hex[:8].upper()}",
        decision=decision,
        stages=[s_intake, s_kyc, s_risk, s_prov],
        extracted=extracted,
        mode="foundry" if settings.use_foundry else "mock",
    )
