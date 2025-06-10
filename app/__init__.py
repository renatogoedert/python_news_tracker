#the package initialisator
#used for setting up configuration, initialize extensions and register blueprints
from flask import Flask
from flasgger import Swagger

from .extensions import db
from .tasks import add_news_from_independent_rss
from .routes.article_routes import article_bp
from .routes.author_routes import author_bp
from .config import Config

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Swagger(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(article_bp)
    app.register_blueprint(author_bp)


    scheduler = BackgroundScheduler()
    scheduler.add_job(
        add_news_from_independent_rss, 
        IntervalTrigger(minutes=15),
        args=[app.app_context()],     
        id='independent_news_scraper',
        replace_existing=True
    )
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())


    return app
