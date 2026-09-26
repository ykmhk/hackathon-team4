"""Routes for the symptom checker feature."""

from flask import Blueprint, render_template


symptom_checker = Blueprint("symptom_checker", __name__)


@symptom_checker.route("/symptoms")
def symptoms():
    """Render the symptom assessment page."""
    return render_template("index.html")
