FROM python:3.9-slim

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY requirements.txt .

RUN pip install --upgrade pip && \
    cat requirements.txt | xargs -n 1 -L 1 pip install --timeout 60 --no-cache-dir && \
    apt-get update && apt-get install -y wget