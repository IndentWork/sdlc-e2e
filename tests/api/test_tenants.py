import uuid
import httpx


def _org() -> str:
    """Generate a unique GitHub org slug for each test to avoid unique-constraint conflicts."""
    return f"test-org-{uuid.uuid4().hex[:8]}"


def test_create_tenant_returns_id_name_and_github_org(client: httpx.Client, created_tenant_ids: list[str]):
    """POST /tenants creates a tenant and returns id, name, and github_org."""
    name = f"e2e-test-{uuid.uuid4()}"
    org  = _org()

    response = client.post("/tenants", json={"name": name, "github_org": org})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == name
    assert body["github_org"] == org
    assert "id" in body
    assert "tenant_key" not in body   # no secret is ever returned

    created_tenant_ids.append(body["id"])


def test_list_tenants_includes_created(client: httpx.Client, created_tenant_ids: list[str]):
    """GET /tenants returns all created tenants including github_org."""
    name = f"e2e-test-{uuid.uuid4()}"
    org  = _org()

    created = client.post("/tenants", json={"name": name, "github_org": org}).json()
    created_tenant_ids.append(created["id"])

    response = client.get("/tenants")
    assert response.status_code == 200
    tenants = response.json()

    matched = [t for t in tenants if t["id"] == created["id"]]
    assert len(matched) == 1
    assert matched[0]["name"] == name
    assert matched[0]["github_org"] == org
