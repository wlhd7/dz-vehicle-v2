# Research: Security Access Control Implementation

## Decision 1: Typer Global Callback
- **Decision**: Use `@admin_app.callback()` in `cli.py`.
- **Rationale**: Typer allows defining a callback for a `Typer` instance (like our `admin_app`). This callback runs before any command within that instance. This ensures that every `admin <command>` is automatically protected without individual checks.
- **Alternatives**: Checking in every function (too repetitive) or using a custom wrapper (harder to maintain).

## Decision 2: FastAPI Dependencies
- **Decision**: Use `dependencies=[Depends(verify_admin_access)]` in `APIRouter` or directly in `app.include_router`.
- **Rationale**: FastAPI's dependency injection system is designed for this. Applying it at the router level ensures all paths under `/admin` are protected consistently.
- **Alternatives**: Middleware (too global, might affect non-admin routes) or individual `Depends` in every function.

## Decision 3: Configuration Loading
- **Decision**: Use `os.getenv` with `python-dotenv` support.
- **Rationale**: standard practice for Python projects. It allows developers to use a `.env` file locally while using system env vars in production.
- **Alternatives**: Hardcoded config (unsafe) or complex config managers (over-engineered).

## Decision 4: Test Strategy
- **Decision**: Use `monkeypatch` in `pytest` to set/unset environment variables.
- **Rationale**: `monkeypatch.setenv` is the idiomatic way to test environment-dependent code in Python.
- **Alternatives**: Mocking `os.getenv` (less realistic).
