def test_calibrate_biometrics_module1(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "bio_user@example.com",
            "full_name": "Bio User",
            "password": "password123"
        }
    )

    response = client.post("/api/v1/codex/module1/calibrate")
    assert response.status_code == 200
    data = response.json()
    assert "recommended_light_exposure_min" in data
    assert "light_timing" in data


def test_resonance_biofeedback(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "bio_feedback_user@example.com",
            "full_name": "Bio Feedback User",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/codex/module1/resonance-biofeedback",
        json={"duration_seconds": 180, "breathing_rate_bpm": 5.5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cycles_completed"] == 16
    assert data["vagustone_increase_pct"] > 0


def test_nlp_semantic_audit(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "nlp_user@example.com",
            "full_name": "NLP User",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/codex/module2/nlp-audit",
        json={"journal_entry": "Hoje tudo deu errado e é impossível recuperar."}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["detected_distortions"]) > 0
    assert len(data["socratic_questions"]) == 3
