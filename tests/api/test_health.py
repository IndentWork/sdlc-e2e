import httpx


def test_health_returns_ok(client: httpx.Client):
    """Health endpoint proves the API is reachable and serving requests."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
