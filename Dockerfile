FROM python:3.12-alpine as builder

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo rust \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip

ENV PATH="/opt/venv/bin:$PATH"

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-alpine as production

RUN apk add --no-cache \
    libffi \
    openssl \
    curl \
    && rm -rf /var/cache/apk/*

RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /opt/venv /opt/venv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY src/ ./src/
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh && \
    chown -R appuser:appgroup /app

USER appuser

WORKDIR /app/src

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

ENTRYPOINT ["../entrypoint.sh"]