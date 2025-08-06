FROM python:3.13-alpine

RUN pip install poetry && python -m venv .venv && source .venv/bin/activate

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root

COPY . .