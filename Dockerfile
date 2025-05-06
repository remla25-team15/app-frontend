FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn==21.2.0

COPY . .

EXPOSE 3000

# Default to production environment
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
