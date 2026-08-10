def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "CODEX VITAE" in response.text
    assert "Os 6 Módulos" in response.text


def test_onboarding_page(client):
    response = client.get("/onboarding")
    assert response.status_code == 200
    assert "Diagnóstico de Performance" in response.text
    assert "O que tem prejudicado de forma mais grave a sua performance ultimamente?" in response.text
    assert "Criar Conta Grátis (14 Dias de Reverse Trial)" in response.text
