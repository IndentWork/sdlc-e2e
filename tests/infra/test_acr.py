from tests.infra._helpers import az


def test_acr_exists(resource_group: str, env: str):
    """Container Registry must exist."""
    result = az("acr", "show", "--name", f"crsdlc{env}", "--resource-group", resource_group)
    assert result["provisioningState"] == "Succeeded"


def test_acr_admin_disabled(resource_group: str, env: str):
    """Admin access must be disabled — pulls only via Managed Identity."""
    result = az("acr", "show", "--name", f"crsdlc{env}", "--resource-group", resource_group)
    assert result["adminUserEnabled"] is False
