from flask import Flask
from flask_cors import CORS
from routes.scrapte_routes import scrape_blueprint
from routes.job_routes import job_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def test():
        return "Server is working"

    # Register Blueprints
    app.register_blueprint(scrape_blueprint)
    app.register_blueprint(job_blueprint)

    return app
