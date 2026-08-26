# sdlc-e2e

End-to-end integration tests for the SDLC platform.

## What it verifies

- Azure infrastructure exists and is configured correctly
- FastAPI is deployed and reachable via public FQDN
- Tenant CRUD works end-to-end
- Security guarantees hold (PostgreSQL not publicly reachable, invalid auth rejected, etc.)

## Test structure

```
tests/
├── api/         Public FastAPI endpoint checks (via httpx)
├── infra/       Azure resource checks (via az CLI)
├── security/    Things that MUST fail — network blocks, invalid auth
└── flows/       Full journey tests — create → get → delete
```

## Running

**Locally against local dev (sdlc-local-dev running):**
```bash
BASE_URL=http://localhost:8000 uv run pytest tests/api tests/flows
```

Infra and security tests need `az login` and target the real Azure environment.

**Against deployed environment (pipeline):**
```
GitHub → Actions → E2E Tests → Run workflow → select DEV or PROD
```

## Adding tests

- New API endpoint → `tests/api/`
- New Azure resource → `tests/infra/`
- New security guarantee → `tests/security/`
- New user journey → `tests/flows/`
