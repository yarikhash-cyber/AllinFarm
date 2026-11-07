# 0002. Монорепо і технології

- Статус: прийнято
- Крок плану: 3

## Контекст

Сайт, API, рушій, одиниці й вікі змінюються разом. Розробляє переважно одна людина з Claude, тож важить простота і швидкий цикл.

## Рішення

Один репозиторій:

| Частина | Технологія |
| --- | --- |
| `apps/web` | SvelteKit (Svelte 5), TypeScript strict, статична збірка (SPA) |
| `apps/api` | FastAPI, Pydantic 2, SQLAlchemy 2, Alembic, psycopg 3 |
| `packages/engine` | Чистий Python 3.13 |
| `packages/units` | Чистий Python 3.13 |
| База | PostgreSQL 18 з PostGIS 3.6 |
| Веб-сервер | Caddy: віддає сайт і проксіює `/api` |
| Пошта для розробки | Mailpit |
| Python-пакети | uv workspace |
| JS-пакети | pnpm workspace |

## Наслідки

- Одна команда `docker compose up --build` піднімає все.
- Усі розрахунки живуть лише в Python (`engine`); сайт їх не дублює.

## Як перевіряється

CI збирає і запускає всю систему в Docker і перевіряє, що `/api/health` відповідає через Caddy і бачить PostGIS.
