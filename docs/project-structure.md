# Project structure

UniHub is split into two applications plus shared documentation. Each folder has one job.

```text
.
├── frontend/                     # React + TypeScript + Vite web app
│   ├── public/                   # Static files served as-is
│   ├── src/
│   │   ├── App.tsx, main.tsx     # Router and app bootstrap
│   │   ├── pages/                # One component per route (Quiz, Packages, Account, ...)
│   │   ├── components/
│   │   │   ├── layout/           # Navbar, Footer, ScrollToTop: used on every page
│   │   │   ├── landing/          # Homepage sections (Hero, Features, AI, Pricing, ...)
│   │   │   ├── packages/         # Package cards, claim/upgrade buttons, PDF download
│   │   │   └── ui/               # shadcn/ui primitives (generated; edit sparingly)
│   │   ├── contexts/             # React context providers (AuthContext)
│   │   ├── hooks/                # Reusable React hooks
│   │   ├── services/             # HTTP clients for the backend API
│   │   ├── lib/                  # Framework-free helpers (packages, pending quiz, PDF, cn)
│   │   ├── types/                # Shared TypeScript types
│   │   ├── assets/               # Images imported by components
│   │   └── test/                 # Vitest setup and tests
│   ├── index.html
│   ├── package.json              # npm scripts: dev, build, lint, test
│   └── vite.config.ts            # Dev server (port 3000) and /api proxy to :8084
│
├── backend/                      # FastAPI + SQLAlchemy + SQLite API
│   ├── app/
│   │   ├── main.py               # FastAPI app, CORS, startup, router registration
│   │   ├── api/
│   │   │   ├── schemas.py        # Request/response models
│   │   │   ├── serializers.py    # Engine results -> JSON
│   │   │   └── routes/           # system, auth, quiz, universities, packages
│   │   ├── core/                 # security.py (JWT, hashing), packages.py (tiers and features)
│   │   ├── db/                   # database.py (engine, ORM models), queries.py, persistence.py
│   │   ├── domain/               # models.py: Pydantic domain models and enums
│   │   ├── quiz/                 # initial.py and extended.py question flows
│   │   └── matching/             # engine.py (initial) and refined_engine.py (program-level)
│   ├── data/                     # unihub.db (seeded app database); test DBs are generated
│   ├── scripts/                  # run_mvp.py (CLI flow), manual_test_scenarios.py
│   ├── tests/
│   │   ├── initial_quiz/         # Initial quiz + basic matching engine
│   │   └── extended_quiz/        # Extended quiz, refined matching, DB queries
│   ├── requirements.txt          # Runtime dependencies
│   ├── requirements-dev.txt      # + pytest, pytest-cov, httpx
│   ├── pytest.ini
│   └── start_api.sh
│
├── docs/                         # All project documentation (see docs/README.md)
├── CLAUDE.md                     # Working agreement for AI agents
└── README.md                     # Setup and overview
```

## Where new code goes

| You are adding… | Put it in |
| --- | --- |
| A new page/route | `frontend/src/pages/` and register it in `App.tsx` |
| A component used by one area | the matching `frontend/src/components/<area>/` folder (create a new area folder if none fits) |
| A call to the backend | `frontend/src/services/` |
| A new API endpoint | a router in `backend/app/api/routes/`, with its models in `api/schemas.py` |
| Business logic (quiz, scoring) | `backend/app/quiz/` or `backend/app/matching/` (keep it free of FastAPI) |
| DB tables or queries | `backend/app/db/` |
| LLM integration | `backend/app/llm/` (see `docs/tasks/llm-foundation.md`) |
| A design decision | `docs/decisions/NNNN-title.md` |

## Commands

| Task | Command |
| --- | --- |
| Frontend dev server | `cd frontend && npm install && npm run dev` |
| Frontend checks | `cd frontend && npm run lint && npm run typecheck && npm test && npm run build` |
| Backend server | `cd backend && pip install -r requirements.txt && uvicorn app.main:app --port 8084 --reload` |
| Backend tests | `cd backend && pip install -r requirements-dev.txt && pytest` |

CI (`.github/workflows/ci.yml`) runs exactly these checks on every pull request and on pushes to `main`. All of them must pass.
