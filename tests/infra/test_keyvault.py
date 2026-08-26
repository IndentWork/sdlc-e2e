from tests.infra._helpers import az


def test_keyvault_exists_with_rbac(resource_group: str, env: str):
    """Key Vault must use RBAC (not access policies) — modern approach."""
    result = az("keyvault", "show", "--name", f"kv-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["properties"]["enableRbacAuthorization"] is True


def test_postgres_admin_password_secret_exists(env: str):
    """
    The PostgreSQL admin password secret must exist in Key Vault.
    Uses list (metadata only) instead of show (value) — the test caller
    may not have Secrets User role and should not need it.
    """
    result = az("keyvault", "secret", "list", "--vault-name", f"kv-sdlc-base-{env}")
    secret_names = [s["name"] for s in result]
    assert "postgres-admin-password" in secret_names
