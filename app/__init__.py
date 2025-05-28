from flask import Flask
from .extensions import db
from .routes.article_routes import article_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    app.register_blueprint(article_bp)

    return app
