from flask import Flask

from music.adapters.memory_repository import MemoryRepository
from music.adapters.repository_populate import populate_repository
from music.home import home_blueprint
from music.authentication import authentication_blueprint
from music.favourites.views import favourites_blueprint
from music.reviews import reviews_blueprint
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)

    # Load the normal application settings from config.py and local .env.
    app.config.from_object("config.Config")

    if test_config is not None:
        app.config.from_mapping(test_config)

    csrf.init_app(app)

    if app.config.get("REPOSITORY") is None:
        repository = MemoryRepository()
        populate_repository(repository)
        app.config["REPOSITORY"] = repository

    from music.tracks import tracks_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(tracks_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(favourites_blueprint)
    app.register_blueprint(reviews_blueprint)
    return app
