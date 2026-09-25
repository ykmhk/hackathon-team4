"""Authentication blueprint for registration, login, and logout."""

from flask import Blueprint


authentication_blueprint = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
)


from main.authentication import views