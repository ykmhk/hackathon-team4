from flask import Blueprint, render_template, redirect, url_for, session, request, flash

import medical_diary.authentication.services as services
from medical_diary.adapters.repository import repo_instance

authentication_blueprint = Blueprint("authentication_bp", __name__, url_prefix="/authentication")


@authentication_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        try:
            user = services.authenticate_user(username, password, repo_instance)
            session.clear()
            session["username"] = user.username
            return redirect(url_for("records_bp.records"))
        except services.AuthenticationException:
            flash("Incorrect username or password.")

    return render_template("authentication/login.html")


@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter a username and password.")
        else:
            try:
                services.add_user(username, password, repo_instance)
                return redirect(url_for("authentication_bp.login"))
            except services.NameNotUniqueException:
                flash("That username is already taken.")

    return render_template("authentication/register.html")


@authentication_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home_bp.home"))
