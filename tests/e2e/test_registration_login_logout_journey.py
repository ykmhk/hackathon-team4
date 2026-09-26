def test_user_can_register_login_and_logout(client):
    # Step 1: The user registers a new account.
    register_response = client.post(
        "/authentication/register",
        data={
            "username": "testuser",
            "password": "TestPassword123",
        },
        follow_redirects=False,
    )

    assert register_response.status_code == 302
    assert register_response.headers["Location"].endswith(
        "/authentication/login"
    )

    # Step 2: The user logs in with the registered account.
    login_response = client.post(
        "/authentication/login",
        data={
            "username": "testuser",
            "password": "TestPassword123",
        },
        follow_redirects=False,
    )

    assert login_response.status_code == 302
    assert login_response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert session["username"] == "testuser"

    # Step 3: The user logs out.
    logout_response = client.post(
        "/authentication/logout",
        follow_redirects=False,
    )

    assert logout_response.status_code == 302
    assert logout_response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert "username" not in session
