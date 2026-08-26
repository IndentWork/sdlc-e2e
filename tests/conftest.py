"""
Shared fixtures for e2e tests.

Environment variables:
  BASE_URL     — public FQDN of the deployed FastAPI (required for API tests)
  ENV          — dev or prod (defaults to dev, used for infra tests)
  RESOURCE_GROUP — resource group to check (defaults to rg-sdlc-base-{ENV})
"""
import os
import httpx
import pytest


@pytest.fixture(scope="session")
def env() -> str:
    return os.environ.get("ENV", "dev")


@pytest.fixture(scope="session")
def resource_group(env: str) -> str:
    return os.environ.get("RESOURCE_GROUP", f"rg-sdlc-base-{env}")


@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.environ.get("BASE_URL")
    if not url:
        pytest.skip("BASE_URL not set — skipping API tests")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def client(base_url: str) -> httpx.Client:
    """Shared HTTP client for the whole test session — connection reuse."""
    with httpx.Client(base_url=base_url, timeout=30.0) as c:
        yield c


@pytest.fixture
def created_tenant_ids(client: httpx.Client):
    """
    Track tenant IDs created during a test and delete them after the test.
    Usage:
        def test_foo(client, created_tenant_ids):
            r = client.post("/tenants", json={"name": "t1"})
            created_tenant_ids.append(r.json()["id"])
    """
    ids: list[str] = []
    yield ids

    # Cleanup — delete every tenant this test created
    for tenant_id in ids:
        try:
            client.delete(f"/tenants/{tenant_id}")
        except Exception:
            pass  # best-effort cleanup
