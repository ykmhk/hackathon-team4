def test_anonymous_user_can_view_favourites_page(client):
    response = client.get("/favourites")

    assert response.status_code == 200

    page = response.get_data(as_text=True)

    assert "Build your own collection." in page
    assert "Log In" in page
    assert "Create an Account" in page
