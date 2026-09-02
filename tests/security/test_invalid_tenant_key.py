"""
Security tests for GitHub OIDC auth on POST /index.

These tests verify that the endpoint rejects requests correctly without a valid token.
A real GitHub OIDC token cannot be generated outside a GitHub Actions runner,
so positive-path auth tests (valid token → 200) are covered by the integration
workflow in sdlc-tenant/sdlc-config.
"""
import httpx


def test_index_rejects_missing_authorization_header(client: httpx.Client):
    """POST /index with no Authorization header must return 422 (missing required header)."""
    response = client.post("/index", json={"project_name": "foo", "repos": ["repo1"]})
    assert response.status_code == 422


def test_index_rejects_non_bearer_scheme(client: httpx.Client):
    """POST /index with Basic auth scheme must return 401."""
    response = client.post(
        "/index",
        json={"project_name": "foo", "repos": ["repo1"]},
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
    )
    assert response.status_code == 401
    assert "Bearer" in response.json()["detail"]


def test_index_rejects_malformed_jwt(client: httpx.Client):
    """POST /index with a Bearer token that is not a valid JWT must return 401."""
    response = client.post(
        "/index",
        json={"project_name": "foo", "repos": ["repo1"]},
        headers={"Authorization": "Bearer this-is-not-a-jwt"},
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]


def test_index_rejects_missing_body_fields(client: httpx.Client):
    """POST /index without required body fields returns 422 regardless of auth."""
    response = client.post(
        "/index",
        json={},
        headers={"Authorization": "Bearer fake-token"},
    )
    assert response.status_code == 422
