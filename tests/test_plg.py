def test_reverse_trial_registration(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "reverse_trial@example.com",
            "full_name": "Reverse Trial User",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["is_pro"] is True  # Reverse Trial Pro active from day 1!


def test_burnout_auditor_lead_magnet(client):
    response = client.post(
        "/api/v1/growth/burnout-audit",
        json={
            "email": "lead@example.com",
            "avg_sleep_hours": 5.5,
            "weekly_work_hours": 60,
            "perceived_stress_level": 9
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["lead_email"] == "lead@example.com"
    assert data["burnout_risk_score"] > 50.0
    assert "recommended_module" in data


def test_ulysses_contract_creation(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "ulysses@example.com",
            "full_name": "Ulysses User",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/codex/module4/ulysses-contract",
        json={
            "contract_title": "Bloqueio de Redes Sociais",
            "commitment_details": "Nenhum acesso a Instagram até as 18h",
            "penalty_financial_cents": 5000
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["crypto_signature"]) == 64  # SHA-256 length
