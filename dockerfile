FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

COPY . .

RUN pip install poetry \
 && poetry install --no-interaction --no-ansi

EXPOSE 80

ENTRYPOINT ["sh", "-c", "poetry run alembic upgrade head && exec poetry run uvicorn src.app:app --host 0.0.0.0 --port 80"]
