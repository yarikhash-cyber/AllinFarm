# AllinFarm

Відкрита система рішень для рослинництва. Вона допомагає господарству обрати технологію з найкращим співвідношенням прибутку й ризику: від стану поля до техкарти, складу і списку закупівлі.

Погода в агрономії є випадковим чинником, тому система показує не одне число, а розподіл результатів за роками погоди. Поле для неї є довгим активом зі своїм станом, а сезон лише змінює цей стан.

## Стан проєкту

Будуємо каркас системи і дизайн на зразкових даних. Справжні агрономічні норми, каталоги й ціни наповнюються після того, як каркас прийнято. Розробка поки йде локально, без сервера.

## Запуск на своєму комп'ютері

Потрібен лише [Docker Desktop](https://www.docker.com/products/docker-desktop/).

- **Windows:** двічі клацнути `start.cmd` у папці проєкту. Покрокова інструкція: [docs/run-on-windows.md](docs/run-on-windows.md).
- **macOS, Linux:** у папці проєкту виконати `docker compose up --build`.

Після запуску відкрийте <http://localhost:8080>. Листи, які надсилає система, видно в поштовій скриньці для розробки на <http://localhost:8025>.

## Як влаштований репозиторій

| Папка | Що там |
| --- | --- |
| `apps/web` | Сайт: SvelteKit, TypeScript |
| `apps/api` | API: FastAPI, Python |
| `packages/engine` | Рушій розрахунків: чиста бібліотека Python без бази й мережі |
| `packages/units` | Одиниці виміру: зберігання в базових одиницях, показ у вибраному наборі |
| `knowledge` | Вікі: агрономічні норми й статті з джерелами |
| `infra` | Налаштування контейнерів і веб-сервера |
| `docs` | Рішення (ADR), словник, інструкції |

Для розробників: [CONTRIBUTING.md](CONTRIBUTING.md).

## Ліцензії

- Код: [GNU AGPL-3.0-or-later](LICENSE).
- Вікі в папці `knowledge`: [CC BY-SA 4.0](knowledge/LICENSE).
- Внески сторонніх людей приймаються за угодою [CLA](CLA.md).

---

**English.** AllinFarm is an open-source decision system for crop farming: field state, technology maps, stock and purchasing, with weather-driven risk. Code is AGPL-3.0-or-later, the knowledge base is CC BY-SA 4.0. Run it locally with `docker compose up --build` and open <http://localhost:8080>.
