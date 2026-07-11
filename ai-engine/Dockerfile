FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8100
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8100/health || exit 1

CMD ["uvicorn", "ai_engine.serve:app", "--host", "0.0.0.0", "--port", "8100"]
