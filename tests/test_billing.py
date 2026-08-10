def test_checkout_session(client):
    # Register & Login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "billinguser@example.com",
            "full_name": "Billing User",
            "password": "password123"
        }
    )

    response = client.post("/api/v1/billing/checkout")
    assert response.status_code == 200
    data = response.json()
    assert "checkout_url" in data
    assert "session_id" in data
