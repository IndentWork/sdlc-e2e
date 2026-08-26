from tests.infra._helpers import az


def test_postgres_server_exists(resource_group: str, env: str):
    """PostgreSQL Flexible Server must exist."""
    result = az("postgres", "flexible-server", "show", "--name", f"psql-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["state"] == "Ready"
    assert result["version"] == "16"


def test_postgres_public_access_disabled(resource_group: str, env: str):
    """PostgreSQL must be VNet-integrated only — no public network access."""
    result = az("postgres", "flexible-server", "show", "--name", f"psql-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["network"]["publicNetworkAccess"] == "Disabled"


def test_postgres_azure_ad_auth_enabled(resource_group: str, env: str):
    """Managed Identity passwordless connection requires AD auth."""
    result = az("postgres", "flexible-server", "show", "--name", f"psql-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["authConfig"]["activeDirectoryAuth"] == "Enabled"
