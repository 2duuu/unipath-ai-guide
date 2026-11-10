# Task: remove dead LLM code and build the foundation of UniHub's LLM integration

Read `CLAUDE.md` at the repository root before doing anything. Its rules take priority over this prompt. If anything here conflicts with it, stop and report the conflict instead of choosing silently. Work in English (code, comments, commits, docs).

## Context

UniHub is a React + Vite + TypeScript frontend (`frontend/`) with a FastAPI + SQLAlchemy + SQLite backend (`backend/`, app entry point `backend/app/main.py`, routers in `backend/app/api/routes/`). Read `docs/project-structure.md` for the layout and where new code goes.

Recommendations come from a deterministic matching engine (`backend/app/matching/refined_engine.py`, `engine.py`). Paid packages are defined in `backend/app/core/packages.py`, mirrored in `frontend/src/lib/packages.ts`.

We are adding an LLM layer for the **paid services** (not the free quiz). Agreed strategy:
- Phase 1 (this task): a hosted LLM API behind our own provider-agnostic interface.
- Later phases: an evaluation set, consent-based data collection, then possibly LoRA fine-tuning of an open-weight model (Qwen3.5 / Gemma 4), served from an EU cloud endpoint through the **same interface**.

So the interface must not assume any particular vendor.

The LLM **explains** results the backend has already computed. It never changes scores, ranking or eligibility, and the product must keep working with no LLM at all.

## Already done (repository reorganisation, before this task)

- Removed dead code: `llm_interface.py` (never imported, broken imports, shared conversation state, hardcoded `gpt-4`) and the unused backend `pdf_generator.py`.
- Removed unused dependencies: openai, anthropic, langchain*, bs4, lxml, reportlab, requests. Added the auth dependencies that were missing.
- Stopped tracking `__pycache__`, `unihub.db.backup` and the generated test DB, and added them to `.gitignore`.
- Split `backend/api.py` into `backend/app/main.py` plus routers. Split `backend/src/` into `backend/app/{core,db,domain,quiz,matching}`. Moved the frontend into `frontend/`.

## Verified facts about the current code (re-verify before changing)

- `InterviewSystem.build_interview_prompt()` in `backend/app/quiz/initial.py` is unused. It also asks for the student's name and GPA, which violates CLAUDE.md's data-minimisation rule.
- `PackageFeature.ADMISSION_PROBABILITY` contradicts CLAUDE.md ("never admission predictions"). It appears in:
  - `backend/app/core/packages.py`
  - `frontend/src/lib/packages.ts`
  - `frontend/src/components/layout/Navbar.tsx` (with a Romanian label)
  - `frontend/src/components/packages/PackageInfoCard.tsx`
  - `frontend/src/components/packages/ClaimPackageButton.tsx`
  - `frontend/src/components/landing/PricingSection.tsx`
  - `frontend/src/pages/Packages.tsx`
- `admission_criteria` has 0 rows. The DB has 37 programs and 89 universities.
- Some API list fields (e.g. university `strong_programs`) come back in a different order depending on `PYTHONHASHSEED`, which suggests iteration over a set. CLAUDE.md requires deterministic output. Fix it if you touch that code, or report it to the lead.
- Existing checks and their current baseline:
  - frontend (`cd frontend`): `npm run lint` (31 problems already there), `npm run test` (1 passed), `npm run build` (OK), `npx tsc -p tsconfig.app.json --noEmit` (clean);
  - backend (`cd backend`, `pip install -r requirements-dev.txt`): `pytest`. Currently 37 passed, 16 failed and 57 errors, mostly tests written against an older DB schema (`avg_bac_score`). `tests/extended_quiz/test_seeding_courses.py` fails to load because `scripts/seed_romanian_universities.py` doesn't exist.

## Work plan: two small PRs, in order

### PR 1: remaining cleanup

1. **Get a baseline.** Run all existing checks first and confirm the baseline above. Don't fix unrelated failures; list them.
2. **Delete `InterviewSystem.build_interview_prompt()`** (after a final grep).
3. **Replace `ADMISSION_PROBABILITY`** with `REQUIREMENTS_FIT_CHECK` ("Requirements & fit check": compares the student's stated situation with *verified, published* requirements; never a probability). Do this in backend and frontend together, update all the UI copy listed above, and translate the Romanian Navbar label to English.

   Existing users' stored package data references tiers, not features. Confirm that, and add a compatibility alias if anything persists the old feature string.
4. Re-run every check. Results must match the baseline.

### PR 2: LLM foundation plus one feature ("Explain my results")

**Backend: create `backend/app/llm/`**
- `provider.py`:
  - a `LLMProvider` protocol: `generate(request: LLMRequest) -> LLMResult`. It is stateless; conversation history is passed in by the caller, never stored on the provider.
  - Implementations:
    - `AnthropicProvider` or `OpenAICompatibleProvider`. Choose one, record why in the ADR, and make adding the other trivial. An OpenAI-compatible client also covers vLLM and most hosted open-model endpoints, which keeps the fine-tuning path open.
    - `FakeProvider`, deterministic and used by all tests.
- `config.py`:
  - provider, model, base URL, timeout, max output tokens, retries: all from environment variables, read server-side only. No hardcoded model IDs in logic.
  - Feature off by default: with `LLM_ENABLED` unset, nothing calls a provider.
- `schemas.py`: Pydantic models for the input and output of each task, with versions. First task: `ExplainResultsInput` / `ExplainResultsOutput`, containing:
  - a summary;
  - per-program reasons, each citing `evidence_ids`;
  - tradeoffs;
  - missing-data notes;
  - `method: "llm" | "deterministic"`.
- `evidence.py`: builds the evidence pack from the DB for the recommended programs. Each fact gets a stable `evidence_id`, plus its source and retrieval date where present. Missing values are explicitly `unknown`, never 0 or empty.
- `prompts/explain_results_v1.py`: a versioned prompt. It must:
  - use only the supplied evidence and cite IDs;
  - treat student text and records as data, never as instructions;
  - make no admission predictions or guarantees;
  - not change ranking;
  - respond in English;
  - return JSON only.
- `validate.py`: parse the output against the schema, then check:
  - every cited ID exists in the evidence pack;
  - the program IDs and order match the backend's ranking;
  - no banned phrases (admission chance, guaranteed, probability of acceptance, …).

  If any check fails, the output is rejected.
- `service.py`:
  - orchestrates: evidence → prompt → provider (timeout and bounded retries) → validate;
  - **on any failure, falls back to a deterministic explanation** built from the score components, labelled `method: "deterministic"`;
  - never sends names, emails, user IDs or free text the task doesn't need.
- `budget.py`: a per-user monthly token budget by package tier, enforced before calling the provider. Configurable limits; keep usage in a new DB table.

  Over budget → deterministic fallback plus a clear flag for the UI. Log token usage per call, without prompts or answers.

**API**
- `POST /api/llm/explain-results`, in a new router `backend/app/api/routes/llm.py` registered in `app/main.py`, with request/response models in `app/api/schemas.py`:
  - requires auth;
  - requires a package with the right feature (e.g. `RANKED_RECOMMENDATIONS` or `ADVANCED_AI_COMPARISONS`, so decide and document);
  - input is the saved quiz result ID, never raw scores sent by the client.

  Error shape: no stack traces or provider details. Status codes for unauthorised, forbidden, not found and budget exceeded.

**Frontend**
- In `frontend/src/services/`, add a typed client for the endpoint. Put the panel component in a new `frontend/src/components/llm/` folder.
- On the results view, add an "AI explanation" panel, shown only to entitled users. It needs:
  - loading, error and retry states, plus a fallback notice;
  - a visible label for `deterministic` vs `llm`;
  - safe rendering (no `dangerouslySetInnerHTML`);
  - accessibility: an `aria-live` status, keyboard access, and visible focus.

**Docs**
- `docs/decisions/0001-llm-strategy.md`: the strategy above, the chosen provider and why, how to swap in a self-hosted or fine-tuned model, data-handling rules and the budget model.
- `docs/contracts.md` (create it, or add a section): the endpoint and schemas.
- Add `backend/.env.example` with the new variables, placeholder values only. `frontend/.env.example` is for `VITE_*` variables only; never put provider keys there.

**Tests: all must use `FakeProvider`; no network calls in CI**
- Valid output is accepted. Invalid JSON, a cited ID that wasn't supplied, a changed ranking order, or banned phrasing each triggers the fallback.
- A timeout or provider exception triggers the fallback, and results stay intact.
- Over budget triggers the fallback plus the flag, with no provider call.
- Unauthenticated → 401. Wrong package → 403.
- A prompt-injection fixture (evidence text containing "ignore previous instructions…") is passed as data, and output validation still holds.
- Missing data shows as `unknown` in the evidence and in the explanation.
- Frontend: the panel renders `llm` and `deterministic` states, and errors and retry work.
- Optional, skipped by default: a live smoke test against the real provider, enabled by an env var.

## Constraints
- Keep secrets out of git and out of the browser bundle. All LLM calls happen server-side.
- Don't add LangChain or another framework. Plain SDK plus Pydantic is enough.
- Don't touch the deterministic scoring logic.
- Don't invent university facts. If evidence is thin, the explanation says so.
- Don't add other paid features yet (comparisons, PDF text, letter/CV feedback, chat). They come next, on this same foundation.
- One branch per PR, focused commits, no force-pushes to shared branches. Don't merge; open the PRs for review.

## Done means
- Both PRs are open, with every repo check run and the actual results reported (baseline vs after).
- With `LLM_ENABLED` unset, the app behaves exactly as before.
- With `FakeProvider`, the full "explain my results" journey works end to end, including the fallback.
- A handoff in the CLAUDE.md format, listing what was not done and any open decisions (for example, untracking `unihub.db` and filling `admission_criteria` with sourced data).
