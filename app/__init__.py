#the package initialisator
#used for setting up configuration, initialize extensions and register blueprints
from flask import Flask
from flasgger import Swagger
from .extensions import db
from .routes.article_routes import article_bp
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Swagger(app)

    app.register_blueprint(article_bp)

    return app
