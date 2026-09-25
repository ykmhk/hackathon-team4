from flask import Flask
from flask_wtf.csrf import CSRFProtect

from main.adapters.memory_repository import MemoryRepository
from main.adapters.repository_populate import populate_repository
from main.authentication import authentication_blueprint
from main.home import home_blueprint
from main.symptom_checker import symptom_checker
from dotenv import load_dotenv

load_dotenv()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object("config.Config")

    if test_config is not None:
        app.config.from_mapping(test_config)

    csrf.init_app(app)

    if app.config.get("REPOSITORY") is None:
        repository = MemoryRepository()
        populate_repository(repository)
        app.config["REPOSITORY"] = repository

    from main.items import items_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(items_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(symptom_checker)
    return app
