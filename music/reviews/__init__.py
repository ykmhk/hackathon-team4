"""Review and rating feature package."""

from flask import Blueprint


reviews_blueprint = Blueprint("reviews", __name__)


# Import routes after creating the blueprint so view functions can register on it.
from music.reviews import views
