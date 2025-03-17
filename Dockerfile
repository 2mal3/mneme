FROM python:3.11-alpine

RUN addgroup nonroot && \
    adduser --system -G nonroot --disabled-password nonroot
USER nonroot

WORKDIR /app

COPY requirements.lock .
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY mneme/ mneme/

ENV DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
ENTRYPOINT "python3 -m mneme.main"