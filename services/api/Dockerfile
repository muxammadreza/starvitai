FROM python:3.13-slim
WORKDIR /app

# Install poetry
RUN pip install poetry==2.2.1

COPY services/api/pyproject.toml services/api/poetry.lock* ./

# Install dependencies (no root, no dev)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY services/api/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
