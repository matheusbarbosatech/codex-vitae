def test_get_vapid_public_key(client):
    response = client.get("/api/v1/notifications/vapid-public-key")
    assert response.status_code == 200
    data = response.json()
    assert "public_key" in data
    assert len(data["public_key"]) > 20


def test_subscribe_push_notification(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "push_user@example.com",
            "full_name": "Push User",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/notifications/subscribe",
        json={
            "endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-token-123",
            "keys": {
                "p256dh": "test-p256dh-key-base64",
                "auth": "test-auth-key-base64"
            }
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["endpoint"] == "https://fcm.googleapis.com/fcm/send/test-endpoint-token-123"
    assert data["p256dh"] == "test-p256dh-key-base64"


def test_test_sentinel_push_dispatch(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "sentinel_user@example.com",
            "full_name": "Sentinel User",
            "password": "password123"
        }
    )

    response = client.post("/api/v1/notifications/test-sentinel")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "result" in data


def test_serve_service_worker(client):
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert "self.addEventListener('push'" in response.text
