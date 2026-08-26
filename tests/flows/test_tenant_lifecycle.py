"""Full lifecycle test — create, get, delete, verify deleted."""
import uuid
import httpx


def test_full_tenant_lifecycle(client: httpx.Client):
    """
    Complete tenant lifecycle:
      1. POST /tenants → 201, returns id
      2. GET  /tenants/{id} → 200, returns the tenant
      3. DELETE /tenants/{id} → 204
      4. GET  /tenants/{id} → 404, gone
    Cleanup is inline — no fixture needed because delete is part of the test.
    """
    name = f"e2e-lifecycle-{uuid.uuid4()}"

    # 1. Create
    create_response = client.post("/tenants", json={"name": name})
    assert create_response.status_code == 201
    tenant_id = create_response.json()["id"]

    # 2. Get by id
    get_response = client.get(f"/tenants/{tenant_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == name

    # 3. Delete
    delete_response = client.delete(f"/tenants/{tenant_id}")
    assert delete_response.status_code == 204

    # 4. Verify deleted
    verify_response = client.get(f"/tenants/{tenant_id}")
    assert verify_response.status_code == 404


def test_delete_is_idempotent(client: httpx.Client):
    """Deleting a non-existent tenant returns 204 (idempotent)."""
    fake_id = str(uuid.uuid4())
    response = client.delete(f"/tenants/{fake_id}")
    assert response.status_code == 204


def test_get_missing_tenant_returns_404(client: httpx.Client):
    """GET /tenants/{unknown} returns 404."""
    fake_id = str(uuid.uuid4())
    response = client.get(f"/tenants/{fake_id}")
    assert response.status_code == 404
