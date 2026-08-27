import httpx


def test_index_rejects_missing_tenant_key(client: httpx.Client):
    """POST /index without tenant_key must be rejected by Pydantic validation."""
    response = client.post("/index", json={"project_name": "foo", "repos": []})
    assert response.status_code == 422  # unprocessable entity


def test_index_rejects_invalid_tenant_key(client: httpx.Client):
    """POST /index with a tenant_key that doesn't hash to any tenant must return 401."""
    response = client.post("/index", json={
        "tenant_key": "this-is-a-completely-fake-key-that-does-not-exist",
        "project_name": "foo",
        "repos": ["repo1"],
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid tenant_key"


def test_index_rejects_tampered_tenant_key(client: httpx.Client, created_tenant_ids: list[str]):
    """
    Create a real tenant, then send a modified version of its key.
    Even one changed character must produce a different SHA256 — must be rejected.
    """
    import uuid
    create = client.post("/tenants", json={"name": f"e2e-tamper-{uuid.uuid4()}"}).json()
    created_tenant_ids.append(create["id"])
    real_key = create["tenant_key"]

    tampered = real_key[:-1] + ("A" if real_key[-1] != "A" else "B")

    response = client.post("/index", json={
        "tenant_key": tampered,
        "project_name": "foo",
        "repos": [],
    })
    assert response.status_code == 401
