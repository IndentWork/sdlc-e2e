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
    """
    Shared HTTP client for the whole test session — connection reuse.
    Timeout is 90s to accommodate Azure Container Apps cold starts:
    when scaled to zero, the first request waits for a new container to boot (~30-60s).
    """
    with httpx.Client(base_url=base_url, timeout=90.0) as c:
        # Warm-up: poke /health until it responds so downstream tests have a hot container.
        # Retry every 5s for up to 3 minutes.
        _wait_for_ready(c)
        yield c


def _wait_for_ready(client: httpx.Client, max_wait_seconds: int = 180) -> None:
    """Poll /health until it returns 200, or fail the test session if it never does."""
    import time
    start = time.time()
    last_error = None
    while time.time() - start < max_wait_seconds:
        try:
            response = client.get("/health", timeout=15.0)
            if response.status_code == 200:
                return
            last_error = f"status={response.status_code}"
        except httpx.HTTPError as exc:
            last_error = str(exc)
        time.sleep(5)
    pytest.fail(f"API never became ready within {max_wait_seconds}s. Last error: {last_error}")


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
