def get_logged_in_username(session) -> str | None:
    return session.get("username")
