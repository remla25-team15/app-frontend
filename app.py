import os

import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('DEBUG', 'false').lower() == 'true'
app.config['APP_NAME'] = os.getenv('APP_NAME', 'app-frontend')

APP_SERVICE_URL = os.getenv('APP_SERVICE_URL', 'http://localhost:5000')

@app.route("/api/version")
def api_version():
    return render_template('index.html', app_service_url=APP_SERVICE_URL)

@app.route("/api/version")
def version_proxy():
    response = requests.get(f"{APP_SERVICE_URL}/api/version")
    return jsonify(response.json()), response.status_code

@app.route("/api/predict", methods=["POST"])
def predict_proxy():
    payload = request.get_json()
    response = requests.post(f"{APP_SERVICE_URL}/api/predict", json=payload)
    return jsonify(response.json()), response.status_code

@app.route("/api/feedback", methods=["POST"])
def feedback_proxy():
    payload = request.get_json()
    response = requests.post(f"{APP_SERVICE_URL}/api/feedback", json=payload)
    return "", response.status_code

@app.route("/")
def index():
    return render_template("index.html", app_service_url=APP_SERVICE_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
