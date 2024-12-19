from flask import Flask
from flask_cors import CORS
from controllers.scrape_controller import scrape_bp
from controllers.keyword_controller import keyword_bp
from controllers.adsense_controller import adsense_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(scrape_bp)
    app.register_blueprint(keyword_bp)
    app.register_blueprint(adsense_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)