# UniHub backend

FastAPI + SQLAlchemy + SQLite API for the UniHub quiz, matching engine, accounts and packages.

## Run

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8084 --reload
```

Once running:
- API: <http://localhost:8084>
- Interactive docs: <http://localhost:8084/docs>

`./start_api.sh` does the same steps in one command.

## Test

```bash
pip install -r requirements-dev.txt
pytest
```

`pytest.ini` sets `pythonpath = .`, so run it from `backend/`. The tests create their own SQLite databases under `data/`; those files are ignored by git.

## Layout

| Path | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI app, CORS, startup, router registration |
| `app/api/routes/` | HTTP endpoints, grouped by area (system, auth, quiz, universities, packages) |
| `app/api/schemas.py` | Request/response models |
| `app/core/` | Auth/JWT (`security.py`) and package tiers/features (`packages.py`) |
| `app/db/` | Engine and ORM models (`database.py`), catalog queries (`queries.py`), profile/feedback writes (`persistence.py`) |
| `app/domain/models.py` | Pydantic domain models and enums |
| `app/quiz/` | Initial and extended question flows |
| `app/matching/` | Initial (`engine.py`) and program-level (`refined_engine.py`) matching |
| `scripts/` | Command-line runner and manual scenarios |
| `tests/` | `initial_quiz/` and `extended_quiz/` suites |

See [`../docs/project-structure.md`](../docs/project-structure.md) for the full repository layout.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///backend/data/unihub.db` | SQLAlchemy database URL |
| `JWT_SECRET_KEY` | a development placeholder | **Must** be set to a strong secret outside local development |
