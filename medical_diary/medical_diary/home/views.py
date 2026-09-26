from flask import Blueprint, render_template, redirect, url_for, session

home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route("/")
def home():
    if session.get("username"):
        return redirect(url_for("records_bp.records"))
    return render_template("home/home.html")
