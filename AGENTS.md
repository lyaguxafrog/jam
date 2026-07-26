## Project

**jamlib** — universal Python auth library (JWT/JWS/JWE, PASETO, sessions, OTP, OAuth2).
Single-package, source in `src/jam/`, tests in `tests/`.

## Commands

```bash
uv sync --group tests --all-extras   # install
uv run pytest -x                     # run all tests
uv run pytest tests/modules/jwt/     # run one module's tests
uv run ruff check src/               # lint
uv run ruff format src/              # format
uv run pyrefly                       # typecheck (pyrefly, not mypy/pyright)
```

CI runs: `uv run pytest -x` (no lint/typecheck in CI — run them locally).

## Architecture

- Entry point: `src/jam/__init__.py` exports `Jam` and `BaseJam`.
- `BaseJam` (`src/jam/__base__.py`) defines the abstract interface. `Jam` (`src/jam/instance.py`) is the concrete implementation.
- Each submodule (jwt, sessions, otp, etc.) follows the same pattern: a `__base__.py` with `Base*` interface classes, then implementations.
- Modules are loaded dynamically from config via `__module_loader__`.
- Optional extras: `redis`, `json`, `yaml`, `toml`, `litestar`, `starlette`, `fastapi`, `flask`.

## Style

- Line length: 80.
- Import order: stdlib, libs, `jam.*` — each group separated by 2 blank lines.
- Ruff ignores: `UP009`, `D100`, `UP007` (see `pyproject.toml`).
- Docstrings: Google-style with type specs. Example in current AGENTS.md is authoritative.

## Testing

- Uses `pytest-asyncio`. Async test patterns exist in `tests/`.
- `conftest.py` monkey-patches `TestAsyncJam._async_mock` — be aware if adding async mocks.
- `fakeredis` is a dev dependency for session/redis tests.
