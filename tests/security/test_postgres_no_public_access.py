import socket

import pytest


def test_postgres_not_reachable_from_public_internet(env: str):
    """
    PostgreSQL must be VNet-integrated only. Direct TCP connect to port 5432
    from the public internet (this test runner) must fail — proves the private
    endpoint is enforced.
    """
    host = f"psql-sdlc-base-{env}.postgres.database.azure.com"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    try:
        # If this succeeds, PostgreSQL is publicly reachable — security failure
        sock.connect((host, 5432))
        sock.close()
        pytest.fail(
            f"SECURITY FAILURE: {host}:5432 is reachable from public internet. "
            "PostgreSQL should be VNet-integrated only."
        )
    except (socket.gaierror, socket.timeout, ConnectionRefusedError, OSError):
        # Expected — DNS may not resolve publicly, or connection times out
        pass
