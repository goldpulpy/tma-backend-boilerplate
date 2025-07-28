FROM python:3.12-alpine

RUN apk add --no-cache shadow && \
    groupadd -r appgroup && \
    useradd -r -g appgroup appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appgroup /app

COPY src/ ./src/

WORKDIR /app/src

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh && \
    chown -R appuser:appgroup /app

USER appuser

ENTRYPOINT ["./entrypoint.sh"]