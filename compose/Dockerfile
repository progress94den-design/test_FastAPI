FROM python:3.13-slim

# Системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --upgrade pip\
    && pip install --no-cache-dir poetry
RUN poetry --version

# Рабочая директория
WORKDIR /app

# Poetry файлы
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем код
COPY src ./src
COPY compose/entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uvicorn", "src.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
