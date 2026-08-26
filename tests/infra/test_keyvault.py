from tests.infra._helpers import az


def test_keyvault_exists_with_rbac(resource_group: str, env: str):
    """Key Vault must use RBAC (not access policies) — modern approach."""
    result = az("keyvault", "show", "--name", f"kv-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["properties"]["enableRbacAuthorization"] is True


def test_postgres_admin_password_secret_exists(env: str):
    """The PostgreSQL admin password must be stored in Key Vault."""
    result = az(
        "keyvault", "secret", "show",
        "--vault-name", f"kv-sdlc-base-{env}",
        "--name", "postgres-admin-password",
    )
    assert result["value"]  # secret has a value
    assert len(result["value"]) >= 20  # random_password length was 32
