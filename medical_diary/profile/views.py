from flask import Blueprint, render_template, redirect, url_for, session, request, flash

import medical_diary.adapters.repository as repository
import medical_diary.profile.services as services

profile_blueprint = Blueprint("profile_bp", __name__, url_prefix="/profile")


@profile_blueprint.route("", methods=["GET", "POST"])
def profile():
    username = session.get("username")

    if not username:
        return redirect(url_for("authentication_bp.login"))

    user = services.get_user(username, repository.repo_instance)

    if user is None:
        session.clear()
        flash("Your session has expired. Please log in again.")
        return redirect(url_for("authentication_bp.login"))

    if request.method == "POST":
        services.update_user(user, request.form)
        flash("Profile updated.")
        return redirect(url_for("profile_bp.profile"))

    return render_template("profile/profile.html", user=user)