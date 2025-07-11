FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

ENV PYTHONPATH=/app
ENV API_BASE_URL=http://host.docker.internal:8000
ENV DEV_AGENT_NAME="Developer Agent"
ENV HEARTBEAT_INTERVAL=60
ENV CODE_CHECK_INTERVAL=300

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://host.docker.internal:8000/health')" || exit 1

CMD ["python", "main.py"] 