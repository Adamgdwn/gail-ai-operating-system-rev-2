FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/apps/gail-os-api

EXPOSE 8123

ENV GAIL_OS_STORE_PATH="/app/data/evidence"
ENV PYTHONPATH="/app/packages/uaos-core/src"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]
