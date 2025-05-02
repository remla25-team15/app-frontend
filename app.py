from flask import Flask, render_template
import os

app = Flask(__name__)

APP_SERVICE_URL = os.getenv('APP_SERVICE_URL', 'http://localhost:5000')

@app.route('/')
def index():
    return render_template('index.html', app_service_url=APP_SERVICE_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
