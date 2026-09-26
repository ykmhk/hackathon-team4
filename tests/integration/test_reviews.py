"""Integration tests for authenticated review and rating requests."""

from music.reviews import services


def register_and_log_in(client, username="reviewer"):
    """Create an account and leave the test client authenticated."""
    client.post(
        "/authentication/register",
        data={"username": username, "password": "ValidPassword1"},
    )
    client.post(
        "/authentication/login",
        data={"username": username, "password": "ValidPassword1"},
    )


def test_anonymous_user_is_redirected_before_posting_a_review(client):
    response = client.post("/track/1/review", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/authentication/login")


def test_logged_in_user_can_post_a_review_and_see_the_average(client):
    register_and_log_in(client)

    response = client.post(
        "/track/1/review",
        data={"rating": "5", "review_text": "Excellent test track"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Review posted successfully." in response.data
    assert b"Excellent test track" in response.data
    assert b"5.0 / 5" in response.data


def test_invalid_review_is_not_stored_and_displays_a_form_error(client):
    register_and_log_in(client)

    response = client.post(
        "/track/1/review",
        data={"rating": "5", "review_text": "   "},
    )

    repository = client.application.config["REPOSITORY"]
    track = repository.get_track(1)
    assert response.status_code == 400
    assert b"Please write a review." in response.data
    assert repository.get_reviews_for_track(track) == []


def test_out_of_range_rating_is_not_stored(client):
    register_and_log_in(client)

    response = client.post(
        "/track/1/review",
        data={"rating": "6", "review_text": "This should not be stored"},
    )

    repository = client.application.config["REPOSITORY"]
    track = repository.get_track(1)
    assert response.status_code == 400
    assert b"Not a valid choice." in response.data
    assert repository.get_reviews_for_track(track) == []


def test_zero_rating_is_accepted(client):
    register_and_log_in(client)

    response = client.post(
        "/track/1/review",
        data={"rating": "0", "review_text": "Not for me"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"0.0 / 5" in response.data


def test_track_detail_lists_reviews_newest_first_with_the_correct_average(client):
    register_and_log_in(client)
    repository = client.application.config["REPOSITORY"]
    user = repository.get_user("reviewer")

    services.add_review(user, 1, 3, "Older review", repository)
    services.add_review(user, 1, 5, "Newer review", repository)

    response = client.get("/track/1")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "4.0 / 5" in page
    assert page.index("Newer review") < page.index("Older review")
