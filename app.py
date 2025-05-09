import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()


app = Flask(__name__)

APP_SERVICE_URL = os.getenv("APP_SERVICE_URL", "http://app-service:5000")


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
    port = os.getenv("PORT", 3000)
    debug = os.getenv("DEBUG", "false").lower() == "true"

    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["APP_NAME"] = os.getenv("APP_NAME", "app-frontend")

    app.run(host="0.0.0.0", port=port, debug=debug)
