FROM python:3.13-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first (better Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Default command (can be overridden by docker-compose)
CMD ["celery", "-A", "app.core.celeryapp", "worker", "--loglevel=info"]