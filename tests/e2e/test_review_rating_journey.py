def test_anonymous_user_cannot_post_review(client):
    # An unauthenticated user attempts to review a track.
    response = client.post(
        "/track/1/review",
        data={
            "review_text": "Excellent test track",
            "rating": "5",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/authentication/login")


def test_logged_in_user_can_post_review_and_rating(client):
    # Step 1: The user registers an account.
    client.post(
        "/authentication/register",
        data={
            "username": "reviewer",
            "password": "TestPassword123",
        },
        follow_redirects=True,
    )

    # Step 2: The user logs in.
    client.post(
        "/authentication/login",
        data={
            "username": "reviewer",
            "password": "TestPassword123",
        },
        follow_redirects=True,
    )

    # Step 3: The logged-in user posts a review and rating.
    review_response = client.post(
        "/track/1/review",
        data={
            "review_text": "Excellent test track",
            "rating": "5",
        },
        follow_redirects=True,
    )
    review_page = review_response.get_data(as_text=True)

    assert review_response.status_code == 200
    assert "Excellent test track" in review_page
    assert "5" in review_page

    # Step 4: The review remains visible on the track detail page.
    detail_response = client.get("/track/1")
    detail_page = detail_response.get_data(as_text=True)

    assert detail_response.status_code == 200
    assert "Excellent test track" in detail_page
