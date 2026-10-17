# ShopAPI

REST API для магазина бытовой техники на FastAPI.

Проект реализует работу с клиентами, товарами, поставщиками, категориями и изображениями товаров. Данные хранятся в PostgreSQL, доступ к БД выполняется через SQLAlchemy с использованием Repository pattern.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 17
- SQLAlchemy 2
- asyncpg
- Alembic
- Pydantic
- Docker Compose
- Uvicorn

## Architecture

```text
HTTP Request
    ↓
Router
    ↓
Service
    ↓
Mapper
    ↓
Repository
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

Основные слои проекта:

```text
app/
├── api/v1/          # REST endpoints
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic DTO
├── mappers/         # DTO ↔ ORM
├── repositories/    # Data access layer
├── services/        # Business logic
├── core/            # Config and exceptions
└── db/              # Database configuration
```

## Features

- CRUD-операции для клиентов, товаров и поставщиков
- Поиск клиентов по имени и фамилии
- Пагинация через `limit` и `offset`
- Учёт остатков товаров
- Категории товаров
- Загрузка и получение изображений в бинарном формате
- Централизованная обработка ошибок
- Валидация входных данных через Pydantic
- OpenAPI / Swagger документация
- Миграции базы данных через Alembic

## HTTP responses

API использует:

- `200 OK` — успешный запрос
- `201 Created` — ресурс создан
- `400 Bad Request` — некорректные входные данные
- `404 Not Found` — ресурс не найден
- `409 Conflict` — конфликт с текущим состоянием ресурса

Если endpoint возвращает список и данных нет, возвращается:

```json
[]
```

## Installation

Клонировать репозиторий:

```bash
git clone git@github.com:Ognennyi/fastapi-shop-api.git
cd shop-api
```

Создать и активировать виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать `.env`:

```env
DB_NAME=shop_api
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Запустить PostgreSQL:

```bash
docker compose up -d
```

Применить миграции:

```bash
alembic upgrade head
```

Запустить API:

```bash
uvicorn app.main:app --reload
```

## Swagger

Swagger UI:

```text
http://localhost:8000/swagger/index.html
```

OpenAPI specification:

```text
http://localhost:8000/swagger/openapi.json
```

Все API endpoints используют префикс:

```text
/api/v1/...
```