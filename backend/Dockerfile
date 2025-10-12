FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles

# Collect static files (ignore errors if no static files)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Run with gunicorn pointing to Django's WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--chdir", "/app", "Secret.wsgi:application"]