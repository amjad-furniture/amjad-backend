# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # prevents Python from writing .pyc files
    PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create and set user
RUN adduser --disabled-password --no-create-home django
RUN chown -R django:django /app
USER django

# Expose port
EXPOSE 8000

# Run gunicorn
CMD gunicorn furniture.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2 