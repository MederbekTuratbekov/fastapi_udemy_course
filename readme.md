# 🎓 Online Course Platform API

> Production-ready REST API for an e-learning marketplace —
> JWT auth, OAuth2, course catalog, lessons, reviews, and admin panel.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-async-teal)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)]()
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Problem

EdTech platforms need a structured API to manage course catalogs,
lessons, and learner feedback at scale. Without access control and
review infrastructure, instructors lose visibility into course
performance and learners have no trusted signal for purchase decisions.

---

## What's Built

- **JWT auth** — register / login / logout / token refresh;
  refresh tokens stored in DB, deleted on logout
- **OAuth2** — GitHub and Google via authlib
- **Course catalog** — full CRUD; level (easy / simple / hard),
  type (free / paid), certificate flag, category FK
- **Lessons** — full CRUD per course; video URL, video file, content
- **Reviews** — star rating + text per course, full CRUD
- **Categories** — course taxonomy, full CRUD
- **Admin panel** — sqladmin web UI for all 5 entities

---

## Tech Stack

| Category   | Technology                              |
|------------|-----------------------------------------|
| Language   | Python 3.11                             |
| Framework  | FastAPI, Uvicorn (ASGI)                 |
| ORM        | SQLAlchemy 2.x (Mapped / mapped_column) |
| Validation | Pydantic v2                             |
| Auth       | python-jose (JWT), passlib (bcrypt)     |
| OAuth2     | authlib (GitHub, Google)                |
| Database   | PostgreSQL                              |
| Admin      | sqladmin                                |
| Config     | python-dotenv                           |

---

## Architecture
Client → FastAPI (ASGI / Uvicorn)
↕
APIRouter modules:
auth · course · lesson
review · category · social_auth
↕
SQLAlchemy 2.x ORM → PostgreSQL
↕
sqladmin (admin panel)

Each domain is a separate `APIRouter` module.
Models use SQLAlchemy 2.x `Mapped` typed columns.
Each entity has `CreateSchema` (input) and `GetSchema` (output)
— prevents clients from injecting auto-generated fields.

---

## Key Decisions

**DB-persisted refresh tokens**
Refresh tokens stored in `RefreshToken` table — logout deletes the
record, refresh validates against DB. Immediate revocation, no Redis needed.

**Create / Get schema split**
`CreateSchema` (no id/dates) and `GetSchema` (includes id + timestamps)
keep API contracts explicit and prevent field injection.

**sqladmin for zero-code admin**
`ModelView` subclasses with `column_list` — management panel
for all 5 entities in ~20 lines of code.

---

## Quick Start

```bash
git clone https://github.com/your-username/fastapi-udemy-course
cd fastapi-udemy-course
cp .env.example .env        # SECRET_KEY, DB_URL, OAuth keys
pip install -r requirements.txt
```

```bash
# Create tables
python -c "from udemy_course.db.database import Base, engine; \
           Base.metadata.create_all(engine)"
```

```bash
uvicorn udemy_course.main:udemy --reload
# Swagger UI → http://localhost:8000/docs
# Admin UI   → http://localhost:8000/admin
```

---

## Demo

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ali",
    "last_name": "U",
    "username": "ali",
    "email": "ali@mail.com",
    "password": "pass123"
  }'
```
```json
{"message": "Created Account"}
```

**List courses:**
```bash
curl http://localhost:8000/course/
```
```json
[{
  "id": 1,
  "course_name": "Python Pro",
  "level": "hard",
  "price": 49.99,
  "type_course": "paid",
  "course_certificate": true,
  "category_id": 2,
  "author_id": 1
}]
```

---

## Endpoints Overview

| Method | Endpoint            | Description          |
|--------|---------------------|----------------------|
| POST   | /auth/register      | Register user        |
| POST   | /auth/login         | Login, get tokens    |
| POST   | /auth/logout        | Logout, delete token |
| POST   | /auth/refresh       | Refresh access token |
| GET    | /oauth/github       | GitHub OAuth2        |
| GET    | /oauth/google       | Google OAuth2        |
| CRUD   | /course/            | Course management    |
| CRUD   | /lesson/            | Lesson management    |
| CRUD   | /review/            | Reviews              |
| CRUD   | /category/          | Categories           |

---

## Project Structure
```
fastapi_udemy_course/
├── .gitignore
├── readme.md
└── udemy_course/
    ├── __init__.py
    ├── admin/
    │   ├── __init__.py
    │   ├── setup.py
    │   └── views.py
    ├── alembic.ini
    ├── api/
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── category.py
    │   ├── course.py
    │   ├── lesson.py
    │   ├── review.py
    │   └── social_auth.py
    ├── config.py
    ├── create_secretkey.py
    ├── db/
    │   ├── __init__.py
    │   ├── database.py
    │   ├── models.py
    │   └── schema.py
    ├── main.py
    ├── migrations/
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions/
    │       ├── 2b9621ebe31e_.py
    │       ├── 505d0bfaabd2_.py
    │       ├── de0d22c1f382_.py
    │       └── f5d1e4016fbf_.py
    └── requirements.txt
```
