FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ensure Python can always find your `app/` package
ENV PYTHONPATH=/app
RUN mkdir -p /app/data

RUN mkdir -p /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Environment variables (override in compose or .env)
ENV DATABASE_URL=sqlite+aiosqlite:///./app.db
ENV METRICS_PORT=8001
ENV JWT_SECRET_KEY=change-me
ENV BROKER_URL=amqp://guest:guest@rabbitmq/
ENV REDIS_URL=redis://redis:6379/0

EXPOSE 8000 8001

ENTRYPOINT ["/entrypoint.sh"]