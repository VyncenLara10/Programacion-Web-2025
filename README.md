# Programacion-Web-2025
# Django API Deployment with Docker and PostgreSQL

This project demonstrates how to deploy a Django API using **Docker** and **Docker Compose**, ensuring fast, efficient, and isolated execution.

---

## Project Overview

This setup contains:
- A **Dockerfile** that builds a lightweight Docker image for the Django API.
- A **docker-compose.yml** file that configures both the Django service and a PostgreSQL database service.
- An **.env** file with environment variables for configuration (default credentials are used for this assignment).

---

## Project Structure

project-root/
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── manage.py
└── <Zapatos>/

---

## Requirements

- Docker installed → [Get Docker](https://docs.docker.com/get-docker/)
- Docker Compose installed → [Get Docker Compose](https://docs.docker.com/compose/install/)

---

## Docker Setup

### 1. Environment Variables
Create a file named `.env` in the root of your project:

```bash
# .env file
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=your_secret_key_here
DEBUG=True

# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Expose port 8000
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

docker-compose up --build
Then visit:
[Local Host](http://localhost:8000)

To stop the containers:
docker-compose down
