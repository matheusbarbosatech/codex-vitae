def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["is_pro"] is True  # Reverse Trial Pro enabled on day 1
    assert "access_token" in response.cookies


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "full_name": "User One",
            "password": "password123"
        }
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "full_name": "User Two",
            "password": "password456"
        }
    )
    assert response.status_code == 400
    assert "já está cadastrado" in response.json()["detail"]


def test_login_user(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "loginuser@example.com",
            "full_name": "Login User",
            "password": "mypassword123"
        }
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": "mypassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
