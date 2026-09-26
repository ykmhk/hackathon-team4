def test_anonymous_user_cannot_add_favourite(client):
    # An unauthenticated user attempts to add a favourite.
    response = client.post(
        "/track/1/favourite",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logged_in_user_can_add_and_remove_favourite(client):
    # Step 1: The user registers an account.
    client.post(
        "/authentication/register",
        data={
            "username": "musicfan",
            "password": "TestPassword123",
        },
        follow_redirects=True,
    )

    # Step 2: The user logs in.
    client.post(
        "/authentication/login",
        data={
            "username": "musicfan",
            "password": "TestPassword123",
        },
        follow_redirects=True,
    )

    # Step 3: The user adds the track to their favourites.
    add_response = client.post(
        "/track/1/favourite",
        follow_redirects=True,
    )

    assert add_response.status_code == 200

    # Step 4: The track appears in the user's favourites list.
    favourites_response = client.get("/favourites")
    favourites_page = favourites_response.get_data(as_text=True)

    assert favourites_response.status_code == 200
    assert "Test Track" in favourites_page

    # Step 5: The user removes the track from their favourites.
    remove_response = client.post(
        "/track/1/favourite/remove",
        follow_redirects=True,
    )

    assert remove_response.status_code == 200

    # Step 6: The track no longer appears in the favourites list.
    favourites_response = client.get("/favourites")
    favourites_page = favourites_response.get_data(as_text=True)

    assert favourites_response.status_code == 200
    assert "Test Track" not in favourites_page