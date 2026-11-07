# Як працювати з репозиторієм

## Порядок

1. Кожна зміна йде окремою гілкою і pull request у `main`.
2. Pull request проходить автоматичні перевірки: стиль, типи, тести, межі модулів, ліцензії залежностей, пошук паролів у коді, запуск усієї системи в Docker.
3. Зміну приймає власник проєкту.
4. Архітектурне рішення записується коротким ADR у `docs/adr/` у тому самому pull request, де воно стає кодом.

Перед першим внеском прочитайте [CLA.md](CLA.md). Поки текст CLA не перевірив юрист, внески приймаються лише від власника проєкту.

## Середовище розробника

Потрібні Docker, [uv](https://docs.astral.sh/uv/), Node.js 22 і pnpm 10.

```bash
uv sync                     # Python-пакети workspace
pnpm install                # пакети сайту
docker compose up --build   # уся система
```

Для швидкої розробки сайту без перезбирання контейнера:

```bash
docker compose up -d db mailpit api
pnpm -C apps/web dev        # http://localhost:5173, запити /api йдуть на http://localhost:8000
```

## Перевірки локально

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run lint-imports
DATABASE_URL=postgresql+psycopg://allinfarm:allinfarm@localhost:54320/allinfarm uv run pytest
pnpm -C apps/web check && pnpm -C apps/web lint && pnpm -C apps/web build
uv run python scripts/check_licenses.py
```

## Межі модулів

- `packages/units` нічого не імпортує з проєкту.
- `packages/engine` може імпортувати лише `units`, без бази, мережі й веб-фреймворків.
- `apps/api` може імпортувати `engine` і `units`.
- Сайт `apps/web` звертається лише до API і лише через `src/lib/api/`.

Порушення ламає CI.
