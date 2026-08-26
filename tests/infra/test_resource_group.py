from tests.infra._helpers import az


def test_resource_group_exists(resource_group: str):
    """Base resource group must exist — everything else lives in it."""
    result = az("group", "show", "--name", resource_group)
    assert result["name"] == resource_group
    assert result["properties"]["provisioningState"] == "Succeeded"
