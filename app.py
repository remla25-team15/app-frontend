from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration from environment
    app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    app.config['DEBUG'] = os.getenv('DEBUG', 'false').lower() == 'true'
    app.config['APP_NAME'] = os.getenv('APP_NAME', 'app-frontend')
    app.config['APP_SERVICE_URL'] = os.getenv('APP_SERVICE_URL', 'http://localhost:5000')

    @app.route('/')
    def index():
        return render_template('index.html', 
                            app_service_url=app.config['APP_SERVICE_URL'],
                            app_name=app.config['APP_NAME'])

    return app

app = create_app()

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '3000'))
    app.run(host=host, port=port)
