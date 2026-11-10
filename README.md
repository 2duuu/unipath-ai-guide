# UniHub

UniHub is a web application that helps students explore Romanian universities,
faculties, and study programs. Users complete a guided questionnaire and receive
personalised university and program matches. The app also supports accounts,
saved quiz attempts, package selection, feedback, and downloadable results.

The project is a full-stack application:

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, and React Router
- **Backend:** FastAPI, Pydantic, SQLAlchemy, and SQLite
- **Matching:** initial university matching followed by an extended
  program-specific assessment

## User journey

1. Open the quiz and answer the initial profile questions.
2. Review university matches based on the submitted profile.
3. Continue with the extended questionnaire for more specific program matches.
4. Optionally create an account to save attempts and view results later.
5. Select a support package or send feedback about the recommendations.

The main user-facing routes are:

| Route | Purpose |
| --- | --- |
| `/` | Landing page |
| `/cum-functioneaza` | How UniHub works |
| `/quiz` | Guided university and program quiz |
| `/facultati` | Faculties and study options |
| `/pachete` | Available support packages |
| `/pachete/checkout` | Package checkout |
| `/cont` | Authenticated account area |
| `/login` | Sign in |
| `/signup` | Create an account |
| `/contact` | Contact page |

## Requirements

For local development, install:

- Node.js 20 or newer
- npm
- Python 3.11 or newer

## Local development

### 1. Install frontend dependencies

```bash
cd frontend
npm install
```

### 2. Set up and start the backend

**Quickest way.** One command creates `backend/venv`, installs the dependencies and starts the API on port 8084. It works from any directory.

```powershell
# Windows PowerShell
.\backend\start_api.ps1
# if scripts are blocked: powershell -ExecutionPolicy Bypass -File backend\start_api.ps1
```

```bash
# macOS / Linux / Git Bash
./backend/start_api.sh
```

**Manual setup** (if you prefer your own virtual environment). From the repository root on Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

### 3. Start the backend (manual setup)

With the virtual environment activated, run this from the `backend/` directory:

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8084 --reload
```

The backend is available at:

- API: <http://localhost:8084>
- Swagger UI: <http://localhost:8084/docs>
- ReDoc: <http://localhost:8084/redoc>

The database is initialised automatically when the API starts. The default
SQLite database is stored in `backend/data/unihub.db`.

### 4. Start the frontend

In a second terminal:

```bash
cd frontend
npm run dev
```

Open <http://localhost:3000>.

The Vite development server proxies `/api` requests to
`http://localhost:8084`. If the API is hosted elsewhere, create `frontend/.env`
(see `frontend/.env.example`):

```dotenv
VITE_API_BASE_URL=http://localhost:8084
```

## API overview

The frontend communicates with the backend through these primary endpoints:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/questions/initial` | Load the initial quiz |
| `POST` | `/api/submit/initial` | Submit answers and get university matches |
| `GET` | `/api/questions/extended` | Load the extended quiz for a profile |
| `POST` | `/api/submit/extended` | Submit answers and get program matches |
| `POST` | `/api/feedback` | Submit recommendation feedback |
| `GET` | `/api/quiz/results` | Get the authenticated user's results |
| `GET` | `/api/quiz/attempts` | Get saved quiz attempts |
| `POST` | `/api/quiz/save-attempt` | Save a quiz attempt |
| `GET` | `/api/stats` | Get application statistics |

Interactive API documentation is available at <http://localhost:8084/docs>
while the backend is running.

## Project structure

```text
.
├── frontend/          # React + TypeScript + Vite app (pages, components, services, lib)
├── backend/
│   ├── app/           # FastAPI app: api/routes, core, db, domain, quiz, matching
│   ├── data/          # SQLite database
│   ├── scripts/       # CLI runner and manual scenarios
│   └── tests/         # initial_quiz/ and extended_quiz/ suites
├── docs/              # All documentation
└── CLAUDE.md          # Working agreement for AI agents
```

See [`docs/project-structure.md`](docs/project-structure.md) for the detailed
layout and where new code should go. Other documentation:

- [`docs/README.md`](docs/README.md): documentation index
- [`backend/README.md`](backend/README.md): backend setup, layout and configuration
- [`docs/integration/FRONTEND_BACKEND_INTEGRATION.md`](docs/integration/FRONTEND_BACKEND_INTEGRATION.md):
  frontend/backend integration details

## Testing and quality checks

Run the frontend checks from `frontend/`:

```bash
npm test
```

Run the frontend linter:

```bash
npm run lint
```

Run the production frontend build:

```bash
npm run build
```

Run the backend tests from `backend/` after activating the Python environment:

```bash
cd backend
python -m pip install -r requirements-dev.txt
python -m pytest
```

For a quick manual API check:

```bash
curl http://localhost:8084/api/health
curl http://localhost:8084/api/questions/initial
```

## Configuration and security

For production deployments:

- Set a strong, private `JWT_SECRET_KEY` instead of the development default.
- Configure the database location with `DATABASE_URL` when using a managed
  database.
- Set `VITE_API_BASE_URL` to the public API URL when the frontend and backend
  are deployed separately.
- Update the backend CORS allowlist in `backend/app/main.py` to include only trusted
  frontend origins.
- Do not commit `.env` files, credentials, API keys, or production database
  files.

## Deployment notes

There is no deployment configuration in the repository yet. For production, use
HTTPS, persistent database storage, managed secrets, and a production-grade
database if multiple instances or high traffic are expected.
