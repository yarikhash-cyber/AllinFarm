# CLAUDE.md

Rules for Claude sessions working in this repository. The project owner is a crop technologist at an agroholding and answers domain questions personally. Talk to the owner in Ukrainian, in plain words.

## How work moves

- The plan is a list of numbered steps; each step has one task and one concrete result the owner can open. The current plan: "План 2.0: каркас і дизайн" (Claude Doc, https://claude.ai/artifact/RhYFL6NkL3apGwcvyj45Nq).
- One step = one GitHub issue or one pull request. A change = a pull request into `main`; the owner accepts it.
- Plans contain no dates, deadlines, durations or forecasts. Only order, tasks and results.
- An architectural decision is written as a short ADR in `docs/adr/` in the same pull request where it becomes code, and a test holds it.

## Architecture rules (checked in CI)

- `packages/engine` is a pure library: no database, no network, no web framework. It gets everything as input and returns results with a manifest.
- `packages/units` is the lowest layer: it imports nothing from the project.
- `apps/web` talks only to the API, through `src/lib/api/`. No `fetch` elsewhere.
- Everything runs in the same Docker containers locally and on a server (`compose.yaml`). Do not add steps that work only on one machine.
- Sample data is always marked as sample (`is_sample` in the database, «зразок» on screen) and goes through the same formats and validators as real data.

## Domain rules

- **Agronomy sources:** never take agronomic norms from Ukrainian state normatives (ДСТУ, ministry or НААН planned-economy norms). Use research papers with DOI, textbooks, originator and seed-company data, international science. Ukrainian state sources only for legal matters (taxes, pesticide registration, application rules).
- **Units:** store values in base units; display through a unit set chosen by the user (set «Україна»: area in ha, yield only in ц/га, gross harvest in t). The unit set does not depend on region.
- **Regions:** no political borders in agronomy. Agro-zones come only from climate and soil. Countries matter only for law, currency and product market.
- **Data licenses:** core data only under CC BY, CC0 or public domain. Non-commercial sources stay optional and off by default. Every source gets its license documented.
- **Field** is a long-lived asset with a state; seasons change that state. The field journal is append-only.
- **Weather is random.** Show distributions over weather years and risk first, money second.
- **No precision-ag core:** no zones/NDVI/VRA in the core.

## Commands

```bash
docker compose up --build        # whole system: http://localhost:8080, mail: http://localhost:8025
uv sync                          # Python workspace
uv run pytest                    # Python tests (API tests need DATABASE_URL)
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run lint-imports              # module boundaries
pnpm install && pnpm -C apps/web check && pnpm -C apps/web lint && pnpm -C apps/web build
uv run python scripts/check_licenses.py   # dependency licenses
```

## Style

- Python 3.13, strict typing (mypy strict), ruff.
- TypeScript strict, Svelte 5 runes.
- Domain terms follow `docs/glossary.md` in code and on screens.
- Commit messages in English, imperative mood.
