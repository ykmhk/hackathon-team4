def get_user(username: str, repo):
    return repo.get_user(username)


def update_user(user, form) -> None:
    """Update a user's personal, healthcare provider and GP details in place
    from a submitted form. Every field is optional and free text."""
    user.full_name = form.get("full_name", "").strip()
    user.date_of_birth = form.get("date_of_birth", "").strip()

    user.provider_name = form.get("provider_name", "").strip()
    user.provider_address = form.get("provider_address", "").strip()
    user.provider_email = form.get("provider_email", "").strip()
    user.provider_phone = form.get("provider_phone", "").strip()
    user.provider_hours = form.get("provider_hours", "").strip()

    user.gp_name = form.get("gp_name", "").strip()
    user.gp_practice = form.get("gp_practice", "").strip()
    user.gp_email = form.get("gp_email", "").strip()
    user.gp_phone = form.get("gp_phone", "").strip()
