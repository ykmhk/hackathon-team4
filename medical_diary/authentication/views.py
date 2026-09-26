from flask import Blueprint, render_template, redirect, url_for, session, request, flash

import medical_diary.adapters.repository as repository
import medical_diary.authentication.services as services

authentication_blueprint = Blueprint("authentication_bp", __name__, url_prefix="/authentication")


@authentication_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        try:
            user = services.authenticate_user(username, password, repository.repo_instance)
            session.clear()
            session["username"] = user.username
            return redirect(url_for("records_bp.records"))
        except services.AuthenticationException:
            flash("Incorrect username or password.")
            return render_template(
                "authentication/login.html",
                username=username,
            )

    return render_template("authentication/login.html", username="")


@authentication_blueprint.route("/register", methods=["GET", "POST"])
def register():
    submitted_username = request.form.get("username", "").strip() if request.method == "POST" else ""
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not password:
            flash("Please complete all required fields.")

        elif len(username) < 3:
            flash("Username must be at least 3 characters.")

        elif len(password) < 6:
            flash("Password must be at least 6 characters.")

        elif password != confirm_password:
            flash("Passwords do not match.")

        else:
            try:
                services.add_user(username, password, repository.repo_instance)
                user = repository.repo_instance.get_user(username)
                if user is not None and full_name:
                    user.full_name = full_name
                flash("Account created. You can now log in.")
                return redirect(url_for("authentication_bp.login"))

            except services.NameNotUniqueException:
                flash("That username is already taken.")

        return render_template(
            "authentication/register.html",
            username=username,
            full_name=full_name,
        )

    return render_template("authentication/register.html", username="", full_name="")


@authentication_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home_bp.home"))
