# 0003. Межі модулів у CI

- Статус: прийнято
- Крок плану: 5

## Контекст

Коду буде багато, і значну частину пише ШІ. Без жорстких меж модулі починають залежати один від одного, і рушій стає неможливо перевірити окремо.

## Рішення

| Модуль | Може імпортувати | Не може |
| --- | --- | --- |
| `allinfarm_units` | лише стандартну бібліотеку і бібліотеки обчислень | будь-що з проєкту, базу, мережу, веб |
| `allinfarm_engine` | `allinfarm_units` | `allinfarm_api`, SQLAlchemy, psycopg, FastAPI, HTTP-клієнти |
| `allinfarm_api` | `allinfarm_engine`, `allinfarm_units` | — |
| `apps/web` | API через `src/lib/api/` | `fetch` поза `src/lib/api/` |

## Наслідки

Рушій тестується без бази й мережі і може працювати будь-де: у воркері, у тестах, у майбутньому офлайн.

## Як перевіряється

- Python: `lint-imports` (import-linter, налаштування в `pyproject.toml`).
- Сайт: правило ESLint `no-restricted-globals` для `fetch` поза `src/lib/api/`.
