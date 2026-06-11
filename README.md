# Week 12 — Capstone: Build, Demo & Review

[![CI](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone/actions/workflows/ci.yml)

> **Standalone lab** from the *Agentic AI on Azure — Enterprise Master Class* (12 weeks).
> Each lab is an independent, runnable FastAPI starter. Part of the
> [course series](https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure).

---

## 🎯 Learning goal
Ship a production-ready, multi-agent application end-to-end on Azure.

## 🏢 Enterprise use case — "Capstone Project" (Pick one scenario)
Choose a scenario — Customer Onboarding Automation (Banking/Telecom), Financial Transaction Compliance (FinTech), Supply-Chain / Sales-Lead Prioritization (Manufacturing/B2B), or Document Generation Workflow (Legal/Insurance) — and build a multi-agent application that brings together everything from the course.

---

## 🧪 What you'll build (lab)
1. Build a multi-agent app (2–4 coordinating agents) with tools via MCP/OpenAPI.
2. Ground on enterprise data with permission-aware retrieval.
3. Containerize the FastAPI service and deploy to Container Apps/AKS with CI/CD.
4. Wire in identity, observability, evaluation, and guardrails.
5. Write up the architecture and prepare a live demo.

> This starter ships with a **runnable mock** of the endpoint so you can run and test
> immediately, then progressively replace the mock with the real Azure implementation.

## 🏗️ Architect's lens
- Defend your design — pattern choice, deployment target, cost model, security posture, and day-2 operations.

## 🧰 Tech stack
Everything from the course: multi-agent orchestration + MCP/OpenAPI, RAG grounding, containerized FastAPI + CI/CD, identity, observability, and evaluation.

---

## 🚀 Quick start

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) copy the env template — runs in MOCK mode without it
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. Run the API
uvicorn app.main:app --reload
```

Open the interactive docs at **http://127.0.0.1:8000/docs**.

### Try the endpoint
```bash
curl -X POST http://127.0.0.1:8000/api/v1/capstone \
  -H "Content-Type: application/json" \
  -d '{"scenario": "Customer Onboarding Automation for a retail bank."}'
```

### Run the tests
```bash
pytest -q
```

### Run with Docker
```bash
docker build -t agentic-ai-azure-week12-capstone .
docker run -p 8000:8000 agentic-ai-azure-week12-capstone
```

---

## 📁 Project structure
```
agentic-ai-azure-week12-capstone/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app + the /api/v1/capstone endpoint
├── tests/
│   └── test_smoke.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

## 🗺️ Where this fits
This repo covers **Week 12 — Capstone: Build, Demo & Review**. The full 12-week path and reference architecture
live in the master-class companion repo:
**[azure-agentic-ai-masterclass](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass)**.

## 📄 License
MIT — see [`LICENSE`](LICENSE).
