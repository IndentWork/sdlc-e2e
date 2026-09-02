"""
POST /index positive-path notes:

A valid GitHub OIDC token can only be obtained inside a GitHub Actions runner.
The full end-to-end positive path (valid token → 200) is tested by the
integration workflow in sdlc-tenant/sdlc-config — not here.

These tests cover body-level validation only (no auth token involved).
"""
import httpx


def test_index_rejects_missing_project_name(client: httpx.Client):
    """POST /index without project_name returns 422."""
    response = client.post(
        "/index",
        json={"repos": ["repo1"]},
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code == 422


def test_index_rejects_missing_repos(client: httpx.Client):
    """POST /index without repos field returns 422."""
    response = client.post(
        "/index",
        json={"project_name": "foo"},
        headers={"Authorization": "Bearer fake"},
    )
    assert response.status_code == 422
