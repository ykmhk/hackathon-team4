from flask import Flask

import medical_diary.adapters.repository as repository
from medical_diary.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key-change-me",
    )
    if test_config:
        app.config.update(test_config)

    # Wire up a single in-memory repository shared across the app.
    repository.repo_instance = MemoryRepository()
    populate(repository.repo_instance)

    with app.app_context():
        from medical_diary.home.views import home_blueprint
        from medical_diary.authentication.views import authentication_blueprint
        from medical_diary.records.views import records_blueprint
        from medical_diary.profile.views import profile_blueprint

        app.register_blueprint(home_blueprint)
        app.register_blueprint(authentication_blueprint)
        app.register_blueprint(records_blueprint)
        app.register_blueprint(profile_blueprint)

    return app
