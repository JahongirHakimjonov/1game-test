#  Тестовое задание: “Мини-система турниров

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

Создать минимальное backend-приложение на FastAPI, моделирующее регистрацию игроков в турниры. Задание помогает оцени.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/JahongirHakimjonov/1game-test.git
cd 1game-test
cp .env.example .env
```

## 🏃 Usage

Run the project:

```bash
docker compose up -d --build
```

## 📂 Project Structure

```bash
├───.github                      # GitHub-related files (CI/CD workflows, issue templates)
│   ├───ISSUE_TEMPLATE           # Templates for GitHub issues
│   └───workflows                # GitHub Actions workflows (e.g., tests, deployment)
├───alembic                      # Alembic migration scripts for database schema changes
├───deployments                 # Deployment configurations
│   └───compose                 # Docker Compose setups
│       └───fastapi             # FastAPI-specific deployment configs
│           └───celery          # Celery service configuration
│               ├───beat        # Celery beat scheduler setup
│               ├───flower      # Flower UI for Celery monitoring
│               └───worker      # Celery worker configuration
└───src                         # Main application source code
    ├───app                     # FastAPI app code
    │   ├───api                 # API routes and views
    │   ├───core                # Core settings, middlewares, and utilities
    │   │   └───config          # Application settings and environment configs
    │   ├───db                  # Database interaction layer
    │   │   └───models          # SQLAlchemy or Pydantic models
    │   ├───repositories        # Data access layer (e.g., CRUD operations)
    │   └───schemas             # Pydantic schemas for request/response models
    └───tests                   # Unit and integration tests
```

---
## 👨‍💻 Author

**Jahongir Hakimjonov** — Backend Developer

## Contact

Please contact Jahongir Hakimjonov with any questions or concerns regarding this project.

- [GitHub](https://github.com/JahongirHakimjonov)
- [Instagram](https://www.instagram.com/ja_kahn_gir/)
- [Telegram](https://t.me/jakhangir_blog)
---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

# ✅ Summary of Improvements

- Added **badges** (Python version, License, Build Status)
- Cleaned **Usage** into a table
- **Project Structure** tree
