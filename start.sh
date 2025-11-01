#!/bin/bash

if [ ! -f .env ]; then
    cp .env.example .env
fi

set -a
source .env
set +a

HOST=${API_BASE_URL:-0.0.0.0}
PORT=${PORT:-8000}

uvicorn app.main:app --host "$HOST" --port "$PORT" --reload