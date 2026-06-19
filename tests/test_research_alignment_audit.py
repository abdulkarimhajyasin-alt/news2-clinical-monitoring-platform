from fastapi.testclient import TestClient

from app.main import app


def test_alignment_audit_requires_research_view_permission():
    response = TestClient(app).get("/api/research/alignment-audit", headers={"X-Dev-Role": "nurse"})

    assert response.status_code == 403


def test_alignment_audit_matrix_includes_document_groups():
    response = TestClient(app).get("/api/research/alignment-audit", headers={"X-Dev-Role": "researcher"})

    assert response.status_code == 200
    payload = response.json()
    groups = {row["source_document_category"] for row in payload["rows"]}
    assert {"research_proposal", "digital_monitoring_form"}.issubset(groups)
    assert payload["summary"]["implemented_count"] > 0
    assert payload["summary"]["missing_count"] == 0


def test_alignment_audit_does_not_add_broad_hospital_management_requirements():
    response = TestClient(app).get("/api/research/alignment-audit", headers={"X-Dev-Role": "researcher"})

    assert response.status_code == 200
    text = response.text.lower()
    forbidden_terms = ["billing", "invoice", "appointment", "scheduling", "iot", "mobile app", "emr"]
    for term in forbidden_terms:
        assert term not in text
