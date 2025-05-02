# app-frontend


## Build and run app-frontend
cd app-frontend
docker build -t app-frontend .
docker run -p 3000:3000 -e APP_SERVICE_URL=http://localhost:5000 app-frontend