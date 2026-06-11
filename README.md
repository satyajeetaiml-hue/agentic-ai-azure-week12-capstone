# Week 12 — Capstone: Build, Demo & Review

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone/actions/workflows/ci.yml)

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class*.
> Course hub: [azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass).

---

## 🎯 Learning goal
Ship a production-shaped, **multi-agent** application end-to-end.

## 🏢 Capstone scenario — "Customer Onboarding Automation" (Banking/Telecom)
A staged pipeline of cooperating agents: **Intake → KYC/Compliance → Risk → Provisioning**, each with its
own status, producing a single onboarding decision. (The other course scenarios — transaction compliance,
lead prioritization, document generation — follow the same shape.)

## ✅ What this repo implements
A sequential multi-agent pipeline that reuses patterns from across the course:

| Stage | Borrows from | Behavior |
|-------|--------------|----------|
| intake | Wk 1–2 | extract name, ID, amount |
| kyc | Wk 6–7 | screening guardrail (sanction/watchlist/PEP) |
| risk | Wk 6–7 | flag high-value cases for review |
| provisioning | Wk 5 tools | create the account when cleared |

Decision: `onboarded` / `needs_review` / `rejected`. Runnable offline; `FOUNDRY_PROJECT_ENDPOINT`
toggles the reported mode.

## 🚀 Quick start
```bash
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/api/v1/capstone \
  -H "Content-Type: application/json" \
  -d '{"applicant_text": "Name: John Doe, ID-AB7788, requesting a $20,000 account."}'
```
Run tests: `pytest -q`

## 🧪 Capstone deliverables (extend this)
- 2–4 coordinating agents with tools via MCP/OpenAPI.
- Grounding on enterprise data with permission-aware retrieval (Wk 8).
- Containerized FastAPI deployed to Container Apps/AKS with CI/CD (Wk 9).
- Identity, observability, evaluation, and guardrails wired in (Wk 10–11).
- Architecture write-up + live demo.

## 🏗️ Architect's lens
Defend your design — pattern choice, deployment target, cost model, security posture, and day-2 operations.

## 🧰 Tech stack
Everything: multi-agent orchestration + MCP/OpenAPI, RAG grounding, containerized FastAPI + CI/CD,
identity, observability, evaluation.

## 🗺️ Series
Prev: [Week 11](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week11-security) ·
Course hub: [azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass) ·
[All labs](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure)

## 📄 License
MIT — see [`LICENSE`](LICENSE).
