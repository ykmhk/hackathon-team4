"""Integration tests for registration, login, and logout."""

def test_register_page_returns_200_and_displays_registration_form(client):
    """GET /authentication/register renders a page containing form fields."""
    response = client.get("/authentication/register")

    assert response.status_code == 200
    assert b"Create an account" in response.data
    assert b'name="username"' in response.data
    assert b'name="password"' in response.data
    assert b"Register" in response.data


def test_login_page_returns_200_and_displays_login_form(client):
    """GET /authentication/login renders a page containing login fields."""
    response = client.get("/authentication/login")

    assert response.status_code == 200
    assert b"Log in" in response.data
    assert b'name="username"' in response.data
    assert b'name="password"' in response.data


def test_register_valid_user_creates_account_and_redirects_to_login(client):
    """A valid registration stores a user and redirects them to login."""
    response = client.post(
        "/authentication/register",
        data={
            "username": "new_user",
            "password": "ValidPassword1",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/authentication/login")

    repository = client.application.config["REPOSITORY"]
    assert repository.get_user("new_user") is not None

def test_register_duplicate_username_displays_error(client):
    """Registering an existing username keeps the user on the form with feedback."""
    client.post(
        "/authentication/register",
        data={
            "username": "existing_user",
            "password": "ValidPassword1",
        },
    )

    response = client.post(
        "/authentication/register",
        data={
            "username": "existing_user",
            "password": "AnotherValid1",
        },
    )

    assert response.status_code == 200
    assert b"This username is already taken." in response.data

    repository = client.application.config["REPOSITORY"]
    assert repository.get_number_of_users() == 1

def test_register_success_message_is_displayed_after_redirect(client):
    """A successful registration displays clear feedback on the login page."""
    response = client.post(
        "/authentication/register",
        data={
            "username": "flash_user",
            "password": "ValidPassword1",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Account created successfully. Please log in." in response.data

def test_login_valid_user_stores_session_and_redirects_home(client):
    """A valid login creates a session and redirects the user to the home page."""
    client.post(
        "/authentication/register",
        data={
            "username": "login_user",
            "password": "ValidPassword1",
        },
    )

    response = client.post(
        "/authentication/login",
        data={
            "username": "login_user",
            "password": "ValidPassword1",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert session["username"] == "login_user"

def test_login_invalid_credentials_displays_error_without_creating_session(client):
    """Invalid credentials do not log in a user or reveal which value was wrong."""
    client.post(
        "/authentication/register",
        data={
            "username": "existing_user",
            "password": "ValidPassword1",
        },
    )

    response = client.post(
        "/authentication/login",
        data={
            "username": "existing_user",
            "password": "WrongPassword1",
        },
    )

    assert response.status_code == 200
    assert b"Invalid username or password." in response.data

    with client.session_transaction() as session:
        assert "username" not in session

def test_logout_clears_session_and_redirects_home(client):
    """A logged-in user can log out and is returned to the home page."""
    client.post(
        "/authentication/register",
        data={
            "username": "logout_user",
            "password": "ValidPassword1",
        },
    )
    client.post(
        "/authentication/login",
        data={
            "username": "logout_user",
            "password": "ValidPassword1",
        },
    )

    response = client.post("/authentication/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert "username" not in session

def test_logout_requires_login(client):
    """Anonymous visitors are redirected to login instead of logging out."""
    response = client.post("/authentication/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/authentication/login")

def test_logout_displays_confirmation_message_after_redirect(client):
    """Logging out displays clear confirmation on the home page."""
    client.post(
        "/authentication/register",
        data={
            "username": "message_user",
            "password": "ValidPassword1",
        },
    )
    client.post(
        "/authentication/login",
        data={
            "username": "message_user",
            "password": "ValidPassword1",
        },
    )

    response = client.post("/authentication/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"You have been logged out." in response.data

def test_navigation_shows_register_and_login_for_anonymous_user(client):
    """Anonymous users can navigate to the registration and login pages."""
    response = client.get("/")

    assert response.status_code == 200
    assert b'href="/authentication/register"' in response.data
    assert b'href="/authentication/login"' in response.data
    assert b"Log out" not in response.data


def test_navigation_shows_user_and_logout_after_login(client):
    """Authenticated users see their username and a logout action."""
    client.post(
        "/authentication/register",
        data={
            "username": "nav_user",
            "password": "ValidPassword1",
        },
    )
    client.post(
        "/authentication/login",
        data={
            "username": "nav_user",
            "password": "ValidPassword1",
        },
    )

    response = client.get("/")

    assert response.status_code == 200
    assert b"Signed in as: nav_user" in response.data
    assert b'action="/authentication/logout"' in response.data
    assert b"Log out" in response.data

def test_register_invalid_password_displays_error_and_does_not_store_user(client):
    """An invalid password is rejected before the registration service stores a user."""
    response = client.post(
        "/authentication/register",
        data={
            "username": "invalid_password_user",
            "password": "alllowercase1",
        },
    )

    assert response.status_code == 200
    assert (
        b"Password must be at least 8 characters and include an uppercase "
        b"letter, a lowercase letter, and a digit."
    ) in response.data

    repository = client.application.config["REPOSITORY"]
    assert repository.get_number_of_users() == 0