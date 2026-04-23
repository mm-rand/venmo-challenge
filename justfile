set dotenv-load
set dotenv-required

develop:
    uv run fastapi dev app/main.py

check:
    uv run ruff format --check
    uv run ruff check
    uv run ty check

fix:
    uv run ruff format
    uv run ruff check --fix

start-infrastructure:
    docker-compose up -d

stop-infrastructure:
    docker-compose down -v
