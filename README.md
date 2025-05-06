# app-frontend

## Environment Configuration

The application supports different environments through environment variables:

### Environment Variables
- `FLASK_ENV`: Set to 'development' or 'production' (default: 'production')
- `DEBUG`: Enable debug mode with 'true' or 'false' (default: 'false')
- `APP_NAME`: Name of the application (default: 'app-frontend')
- `APP_SERVICE_URL`: URL of the backend service (default: 'http://localhost:5000')
- `HOST`: Host to bind to (default: '0.0.0.0')
- `PORT`: Port to run on (default: '3000')

### Development Setup
```bash
# Using local Python
cp .env.example .env  # Copy example env file and modify as needed
pip install -r requirements.txt
python app.py

# Using Docker
docker build -t app-frontend .
docker run -p 3000:3000 -e FLASK_ENV=development -e DEBUG=true -e APP_SERVICE_URL=http://localhost:5000 app-frontend
```

### Production Setup
In production, the application uses gunicorn as the WSGI server and integrates with Kubernetes service discovery:

```bash
docker run -p 3000:3000 -e FLASK_ENV=production -e APP_SERVICE_URL=http://app-service:5000 app-frontend
```

## Service Discovery

### Development
- Uses direct service URLs configured through environment variables
- Default assumes services running locally or through Docker Compose

### Production (Kubernetes)
- Services discover each other through Kubernetes DNS
- Example: app-service is discovered at `http://app-service:5000`
- Health checks ensure service availability
- NGINX ingress controller handles external traffic routing

## Build and run app-frontend
cd app-frontend
docker build -t app-frontend .
docker run -p 3000:3000 -e APP_SERVICE_URL=http://localhost:5000 app-frontend