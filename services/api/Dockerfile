FROM python:3.13-slim
WORKDIR /app

# Install poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

# Install dependencies (no root, no dev)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
