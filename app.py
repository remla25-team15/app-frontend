import os
import time

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from prometheus_client import Counter, Gauge, Histogram
from prometheus_flask_exporter import PrometheusMetrics

load_dotenv()

app = Flask(__name__)
metrics = PrometheusMetrics(app)

APP_SERVICE_URL = os.getenv("APP_SERVICE_URL", "http://app-service:5000")

# Simple page view counter
page_views_total = Counter(
    'frontend_page_views_total',
    'Total number of page views',
    ['endpoint']
)

prediction_requests_total = Counter(
    "frontend_prediction_requests_total",
    "Total number of prediction requests sent from frontend",
    ["status"],
)

active_users_total = Gauge(
    "frontend_active_users_total", "Total number of active users", ["device_type"]
)

predict_latency = Histogram(
    "frontend_predict_request_duration_seconds",
    "Latency for frontend /api/predict calls",
    buckets=(0.1, 0.25, 0.5, 1, 2, 5),
)

feedback_rating_total = Counter(
    "frontend_feedback_rating_total",
    "Total number of feedbacks classified by type",
    ["feedback_type"],  # "positive" or "negative"
)


@app.route("/api/version")
def version_proxy():
    response = requests.get(f"{APP_SERVICE_URL}/app/api/version")
    return jsonify(response.json()), response.status_code


@app.route("/api/predict", methods=["POST"])
def predict_proxy():
    payload = request.get_json()

    try:
        with predict_latency.time():
            response = requests.post(f"{APP_SERVICE_URL}/app/api/predict", json=payload)
        prediction_requests_total.labels(status=str(response.status_code)).inc()
        return jsonify(response.json()), response.status_code

    except Exception as e:
        prediction_requests_total.labels(status="500").inc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/feedback", methods=["POST"])
def feedback_proxy():
    payload = request.get_json()
    try:
        is_correct = payload.get("is_correct")
        if is_correct is True:
            feedback_rating_total.labels(feedback_type="positive").inc()
        elif is_correct is False:
            feedback_rating_total.labels(feedback_type="negative").inc()
        else:
            feedback_rating_total.labels(feedback_type="unknown").inc()

        response = requests.post(f"{APP_SERVICE_URL}/app/api/feedback", json=payload)
        return "", response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    page_views_total.labels(endpoint='/').inc()
    active_users_total.labels(device_type="desktop").set(4)
    active_users_total.labels(device_type="mobile").inc()
    return render_template("index.html", app_service_url=APP_SERVICE_URL)


if __name__ == "__main__":
    port = os.getenv("PORT", 3000)
    debug = os.getenv("DEBUG", "false").lower() == "true"

    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["APP_NAME"] = os.getenv("APP_NAME", "app-frontend")

    app.run(host="0.0.0.0", port=port, debug=debug)
