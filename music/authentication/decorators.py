"""Reusable access-control decorators for authentication-protected routes."""

from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view):
    """Redirect anonymous visitors to login before allowing a protected action."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("authentication.login"))

        return view(*args, **kwargs)

    return wrapped_view