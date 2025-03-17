FROM python:3.11-alpine

RUN addgroup nonroot && \
    adduser --system -G nonroot --disabled-password nonroot

WORKDIR /app

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

COPY requirements.lock .
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY mneme/ mneme/

ENV DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}

USER nonroot

ENTRYPOINT "./docker-entrypoint.sh"