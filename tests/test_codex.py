def test_list_modules(client):
    response = client.get("/api/v1/codex/modules")
    assert response.status_code == 200
    modules = response.json()
    assert len(modules) == 6
    keys = [m["key"] for m in modules]
    assert "maquina" in keys
    assert "processador" in keys
    assert "tribo" in keys
    assert "combustivel" in keys
    assert "escudo" in keys
    assert "bussola" in keys


def test_generate_plan_authenticated(client):
    # Register & Login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "codexuser@example.com",
            "full_name": "Codex User",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/v1/codex/generate",
        json={
            "module_key": "maquina",
            "user_context": "Desejo otimizar o meu sono e energia matinal."
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["module_key"] == "maquina"
    assert "Codex Vitae" in data["plan_output"]
