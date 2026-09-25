from main import create_app


def test_homepage_uses_generic_skeleton_branding():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Starter App" in page
    assert "Music Library" not in page
