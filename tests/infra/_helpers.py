"""Shared helpers for infra tests — wraps az CLI calls."""
import json
import subprocess


def az(*args: str) -> dict:
    """Run an az command and return parsed JSON."""
    result = subprocess.run(
        ["az", *args, "-o", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"az {' '.join(args)} failed: {result.stderr}")
    return json.loads(result.stdout) if result.stdout.strip() else {}
