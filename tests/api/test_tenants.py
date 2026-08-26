import uuid
import httpx


def test_create_tenant_returns_id_and_name(client: httpx.Client, created_tenant_ids: list[str]):
    """POST /tenants creates a tenant and returns its id and name."""
    name = f"e2e-test-{uuid.uuid4()}"
    response = client.post("/tenants", json={"name": name})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == name
    assert "id" in body

    created_tenant_ids.append(body["id"])


def test_list_tenants_includes_created(client: httpx.Client, created_tenant_ids: list[str]):
    """GET /tenants returns all created tenants."""
    name = f"e2e-test-{uuid.uuid4()}"
    created = client.post("/tenants", json={"name": name}).json()
    created_tenant_ids.append(created["id"])

    response = client.get("/tenants")
    assert response.status_code == 200
    tenants = response.json()

    matched = [t for t in tenants if t["id"] == created["id"]]
    assert len(matched) == 1
    assert matched[0]["name"] == name
