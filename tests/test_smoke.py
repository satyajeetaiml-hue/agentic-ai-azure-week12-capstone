"""Smoke tests for Week 12 — Capstone: Build, Demo & Review."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_endpoint_accepts_input():
    r = client.post("/api/v1/capstone", json={"scenario": "Customer Onboarding Automation for a retail bank."})
    assert r.status_code == 200


def test_endpoint_rejects_empty():
    r = client.post("/api/v1/capstone", json={"scenario": ""})
    assert r.status_code == 422
