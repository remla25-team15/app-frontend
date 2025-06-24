# Stage 1: Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build tools (only in this stage)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies into a temp location
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt gunicorn==21.2.0

# Copy app source
COPY . .

# Stage 2: Runtime-only final image
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app source
COPY --from=builder /app /app

EXPOSE 3000

# Set environment defaults (can be overridden at runtime)
ENV FLASK_ENV=production \
    DEBUG=false \
    HOST=0.0.0.0 \
    PORT=3000

# Use gunicorn in production, Flask dev server in development
CMD if [ "$FLASK_ENV" = "production" ]; then \
    gunicorn --bind $HOST:$PORT app:app; \
    else \
    python app.py; \
    fi
