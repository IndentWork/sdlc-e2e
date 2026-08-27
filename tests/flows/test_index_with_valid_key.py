"""Positive path: create a tenant, use its key to call /index successfully."""
import uuid
import httpx


def test_index_accepts_valid_tenant_key(client: httpx.Client, created_tenant_ids: list[str]):
    """
    End-to-end flow:
      1. Create tenant → receive plaintext tenant_key ONCE
      2. Call POST /index with that key → 200 OK
      3. Response confirms the tenant was recognized
    """
    name = f"e2e-index-{uuid.uuid4()}"
    create = client.post("/tenants", json={"name": name}).json()
    tenant_id = create["id"]
    tenant_key = create["tenant_key"]
    created_tenant_ids.append(tenant_id)

    response = client.post("/index", json={
        "tenant_key": tenant_key,
        "project_name": "test-project",
        "repos": ["repo1", "repo2"],
    })

    assert response.status_code == 200
    body = response.json()
    assert "job_id" in body
    assert name in body["message"]  # message references our tenant name


def test_tenant_key_is_returned_only_at_creation(client: httpx.Client, created_tenant_ids: list[str]):
    """
    The plaintext tenant_key must be returned ONLY at POST /tenants.
    GET /tenants and GET /tenants/{id} must NEVER return it.
    """
    name = f"e2e-key-privacy-{uuid.uuid4()}"
    create = client.post("/tenants", json={"name": name}).json()
    tenant_id = create["id"]
    created_tenant_ids.append(tenant_id)

    # POST response has tenant_key
    assert "tenant_key" in create

    # GET single tenant must NOT include tenant_key
    get_response = client.get(f"/tenants/{tenant_id}").json()
    assert "tenant_key" not in get_response
    assert "sha256_key" not in get_response

    # List of tenants must NOT include tenant_key on any entry
    list_response = client.get("/tenants").json()
    for tenant in list_response:
        assert "tenant_key" not in tenant
        assert "sha256_key" not in tenant
