"""Hermetic tests for the Week 12 capstone onboarding pipeline."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_clean_applicant_onboarded():
    r = client.post(
        "/api/v1/capstone",
        json={"applicant_text": "Name: John Doe, ID-AB7788, requesting a $20,000 account."},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["extracted"]["id_number"] == "AB7788"
    assert body["extracted"]["amount"] == 20000
    assert body["decision"] == "onboarded"
    assert [s["name"] for s in body["stages"]] == ["intake", "kyc", "risk", "provisioning"]


def test_sanction_hit_rejected():
    r = client.post(
        "/api/v1/capstone",
        json={"applicant_text": "Name: Jane Roe, ID-CD1122, on sanction list, $5,000."},
    )
    body = r.json()
    assert body["decision"] == "rejected"
    assert body["stages"][3]["status"] == "skipped"


def test_high_value_needs_review():
    r = client.post(
        "/api/v1/capstone",
        json={"applicant_text": "Name: Big Spender, ID-EF9090, requesting $250k account."},
    )
    body = r.json()
    assert body["extracted"]["amount"] == 250000
    assert body["decision"] == "needs_review"


def test_missing_id_needs_review():
    r = client.post(
        "/api/v1/capstone",
        json={"applicant_text": "Name: No Id, opening a $10,000 account."},
    )
    assert r.json()["decision"] == "needs_review"


def test_validation_rejects_empty():
    assert client.post("/api/v1/capstone", json={"applicant_text": ""}).status_code == 422
