FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV API_BASE_URL=http://host.docker.internal:8000
ENV PO_AGENT_NAME="Product Owner Agent"
ENV HEARTBEAT_INTERVAL=60
ENV STORY_CHECK_INTERVAL=300

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://host.docker.internal:8000/health')" || exit 1

# Run the agent
CMD ["python", "main.py"] 