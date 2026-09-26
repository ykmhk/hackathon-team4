from main import create_app


def test_app_factory_builds():
    app = create_app({"TESTING": True})
    assert app is not None
    assert app.config["TESTING"] is True
