"""Authentication blueprint for registration, login, and logout."""

from flask import Blueprint


authentication_blueprint = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
)


# Import routes after creating the blueprint so view functions can register on it.
from music.authentication import views