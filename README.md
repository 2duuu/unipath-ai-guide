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
- **Deployment:** Docker Compose with Nginx serving the frontend and proxying
  `/api` requests to the backend

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

Docker Desktop can be used instead of installing the frontend and backend
dependencies locally.

## Local development

### 1. Install frontend dependencies

From the repository root:

```bash
npm install
```

### 2. Set up the backend environment

From the repository root on Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m pip install -r backend\api_requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
python -m pip install -r backend/api_requirements.txt
```

### 3. Start the backend

Run this from the repository root:

```bash
python -m uvicorn api:app --app-dir backend --host 0.0.0.0 --port 8084 --reload
```

The backend is available at:

- API: <http://localhost:8084>
- Swagger UI: <http://localhost:8084/docs>
- ReDoc: <http://localhost:8084/redoc>

The database is initialised automatically when the API starts. The default
SQLite database is stored in `backend/data/unihub.db`.

### 4. Start the frontend

In a second terminal, from the repository root:

```bash
npm run dev
```

Open <http://localhost:3000>.

The Vite development server proxies `/api` requests to
`http://localhost:8084`. If the API is hosted elsewhere, create a `.env` file
in the repository root:

```dotenv
VITE_API_BASE_URL=http://localhost:8084
```

The shell helper at `backend/start_api.sh` is intended for Unix-like
environments. On Windows, use the Uvicorn command above.

## Docker Compose

Docker Compose starts both services with the production-style Nginx frontend
and the FastAPI backend:

```bash
docker compose up --build
```

Then open <http://localhost:3000>. The frontend container serves the built
application and proxies API requests to the backend container. Stop the
services with:

```bash
docker compose down
```

The SQLite data directory is mounted from `backend/data`, so database data is
preserved when containers are recreated.

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
├── src/                    # React application
│   ├── components/         # Shared UI and layout components
│   ├── contexts/           # React context providers
│   ├── pages/              # Application routes
│   ├── services/           # API and domain service clients
│   └── types/              # Shared frontend types
├── backend/
│   ├── api.py              # FastAPI application and REST endpoints
│   ├── src/                # Matching, interview, auth, and database logic
│   ├── data/               # SQLite databases
│   └── tests/              # Backend test suites
├── docs/                   # Database, integration, and package documentation
├── public/                 # Static frontend assets
├── Dockerfile              # Multi-stage frontend image
├── docker-compose.yml      # Frontend and backend services
└── vite.config.ts          # Vite development server and API proxy
```

More focused documentation is available in:

- [`docs/README.md`](docs/README.md) — documentation index
- [`docs/integration/FRONTEND_BACKEND_INTEGRATION.md`](docs/integration/FRONTEND_BACKEND_INTEGRATION.md)
  — frontend/backend integration details
- [`backend/docs/README.md`](backend/docs/README.md) — backend documentation
- [`backend/frontend/README.md`](backend/frontend/README.md) — quiz integration
  examples

## Testing and quality checks

Run the frontend test suite:

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

Run backend tests from the repository root after activating the Python
environment:

```bash
python -m pytest backend/tests -v
python -m pytest backend/tests_initial_quiz -v
```

For a quick manual API check:

```bash
curl http://localhost:8084/api/health
curl http://localhost:8084/api/questions/initial
```

## Configuration and security

For production deployments:

- Set a strong, private JWT secret instead of the development value used by
  Docker Compose.
- Configure the database location with `DATABASE_URL` when using a managed
  database.
- Set `VITE_API_BASE_URL` to the public API URL when the frontend and backend
  are deployed separately.
- Update the backend CORS allowlist in `backend/api.py` to include only trusted
  frontend origins.
- Do not commit `.env` files, credentials, API keys, or production database
  files.

## Deployment notes

The included Docker setup is suitable for a single-host deployment behind a
reverse proxy. For production, use HTTPS, persistent database storage, a
managed secret configuration, and a production-grade database if multiple
instances or high traffic are expected.
