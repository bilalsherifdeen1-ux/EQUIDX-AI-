FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8400
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8400/health || exit 1
CMD ["uvicorn", "mobile_api.main:app", "--host", "0.0.0.0", "--port", "8400"]
