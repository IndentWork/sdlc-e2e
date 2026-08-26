from tests.infra._helpers import az


def test_container_app_environment_exists(resource_group: str, env: str):
    """Container App Environment must be VNet-integrated."""
    result = az("containerapp", "env", "show", "--name", f"cae-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["properties"]["provisioningState"] == "Succeeded"
    assert result["properties"]["vnetConfiguration"]["infrastructureSubnetId"]  # non-empty


def test_container_app_running(resource_group: str, env: str):
    """FastAPI Container App must be provisioned."""
    result = az("containerapp", "show", "--name", f"ca-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["properties"]["provisioningState"] == "Succeeded"


def test_container_app_has_managed_identity(resource_group: str, env: str):
    """Container App must have User-Assigned Managed Identity attached."""
    result = az("containerapp", "show", "--name", f"ca-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["identity"]["type"] == "UserAssigned"
    assert len(result["identity"]["userAssignedIdentities"]) == 1


def test_container_app_has_public_ingress(resource_group: str, env: str):
    """FastAPI is the only public endpoint — must have external ingress on 8000."""
    result = az("containerapp", "show", "--name", f"ca-sdlc-base-{env}", "--resource-group", resource_group)
    ingress = result["properties"]["configuration"]["ingress"]
    assert ingress["external"] is True
    assert ingress["targetPort"] == 8000
    assert ingress["fqdn"]  # public FQDN exists
