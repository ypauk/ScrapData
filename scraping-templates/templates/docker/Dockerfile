FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    IS_DOCKER=1 \
    HEADLESS=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium

COPY app/ ./app/
COPY .env* ./

RUN mkdir -p output input

CMD ["python", "-m", "app.main"]
