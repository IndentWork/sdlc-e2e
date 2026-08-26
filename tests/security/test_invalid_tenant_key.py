import httpx
import pytest


def test_index_rejects_missing_tenant_key(client: httpx.Client):
    """POST /index without tenant_key must be rejected by Pydantic validation."""
    response = client.post("/index", json={"project_name": "foo", "repos": []})
    assert response.status_code == 422  # unprocessable entity


@pytest.mark.skip(reason="Tenant verification not yet implemented in POST /index")
def test_index_rejects_invalid_tenant_key(client: httpx.Client):
    """POST /index with a tenant_key that doesn't exist in DB must return 401."""
    response = client.post("/index", json={
        "tenant_key": "invalid-key-that-does-not-exist",
        "project_name": "foo",
        "repos": ["repo1"],
    })
    assert response.status_code == 401
