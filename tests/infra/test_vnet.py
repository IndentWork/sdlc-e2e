from tests.infra._helpers import az


def test_vnet_exists_with_correct_address_space(resource_group: str, env: str):
    """VNet must exist with the expected /16 address space."""
    result = az("network", "vnet", "show", "--name", f"vnet-sdlc-base-{env}", "--resource-group", resource_group)
    assert result["addressSpace"]["addressPrefixes"] == ["10.0.0.0/16"]


def test_postgres_subnet_has_correct_delegation(resource_group: str, env: str):
    """PostgreSQL subnet must have Microsoft.DBforPostgreSQL/flexibleServers delegation."""
    result = az(
        "network", "vnet", "subnet", "show",
        "--name", f"snet-sdlc-base-{env}-postgres",
        "--vnet-name", f"vnet-sdlc-base-{env}",
        "--resource-group", resource_group,
    )
    assert result["addressPrefix"] == "10.0.1.0/24"
    delegations = result["delegations"]
    assert any(d["serviceName"] == "Microsoft.DBforPostgreSQL/flexibleServers" for d in delegations)


def test_container_app_subnet_has_correct_delegation(resource_group: str, env: str):
    """Container Apps subnet must have Microsoft.App/environments delegation."""
    result = az(
        "network", "vnet", "subnet", "show",
        "--name", f"snet-sdlc-base-{env}-container-app",
        "--vnet-name", f"vnet-sdlc-base-{env}",
        "--resource-group", resource_group,
    )
    assert result["addressPrefix"] == "10.0.2.0/23"
    delegations = result["delegations"]
    assert any(d["serviceName"] == "Microsoft.App/environments" for d in delegations)
