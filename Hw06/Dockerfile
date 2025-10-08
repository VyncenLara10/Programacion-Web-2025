FROM python:3.12-slim AS builder

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

FROM python:3.12-slim

WORKDIR /app

RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --create-home appuser

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]