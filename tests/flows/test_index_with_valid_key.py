"""
POST /index — body validation tests.

Auth (JWT validation) runs before body validation in FastAPI.
Sending an invalid token always returns 401 regardless of the body content.
Body validation (422) is only reachable with a valid OIDC token, which
requires a real GitHub Actions runner — tested via sdlc-tenant/sdlc-config.
"""
import httpx


def test_index_rejects_missing_project_name(client: httpx.Client):
    """POST /index with an invalid token returns 401 — auth runs before body validation."""
    response = client.post(
        "/index",
        json={"repos": ["repo1"]},
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code == 401


def test_index_rejects_missing_repos(client: httpx.Client):
    """POST /index with an invalid token returns 401 — auth runs before body validation."""
    response = client.post(
        "/index",
        json={"project_name": "foo"},
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code == 401
