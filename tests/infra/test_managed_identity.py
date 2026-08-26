from tests.infra._helpers import az


def test_managed_identity_exists(resource_group: str, env: str):
    """Managed Identity for FastAPI must exist."""
    result = az("identity", "show", "--name", f"id-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["name"] == f"id-sdlc-base-{env}"
    assert result["principalId"]  # non-empty
    assert result["clientId"]     # non-empty


def test_managed_identity_has_acr_pull_role(resource_group: str, env: str):
    """Managed Identity must have AcrPull role on the Container Registry."""
    identity = az("identity", "show", "--name", f"id-sdlc-base-{env}", "--resource-group", resource_group)
    principal_id = identity["principalId"]

    acr = az("acr", "show", "--name", f"crsdlc{env}", "--resource-group", resource_group)
    acr_id = acr["id"]

    assignments = az("role", "assignment", "list", "--assignee", principal_id, "--scope", acr_id)
    role_names = [a["roleDefinitionName"] for a in assignments]
    assert "AcrPull" in role_names


def test_managed_identity_is_postgres_ad_admin(resource_group: str, env: str):
    """Managed Identity must be the PostgreSQL Azure AD administrator."""
    # Use ARM REST API — ad-admin subcommand requires an extension not installed by default
    subscription = az("account", "show")["id"]
    url = (
        f"/subscriptions/{subscription}"
        f"/resourceGroups/{resource_group}"
        f"/providers/Microsoft.DBforPostgreSQL/flexibleServers/psql-sdlc-base-{env}"
        f"/administrators?api-version=2023-03-01-preview"
    )
    result = az("rest", "--method", "get", "--url", url)
    admin_object_ids = [a["properties"]["objectId"] for a in result.get("value", [])]

    identity = az("identity", "show", "--name", f"id-sdlc-base-{env}", "--resource-group", resource_group)
    assert identity["principalId"] in admin_object_ids
