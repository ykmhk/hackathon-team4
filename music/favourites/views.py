from flask import Blueprint, current_app, render_template, session, redirect, url_for
from music.authentication.decorators import login_required
from music.favourites import services
favourites_blueprint = Blueprint("favourites_bp", __name__)

@favourites_blueprint.route("/favourites")

def favourites():
    repository = current_app.config["REPOSITORY"]
    user = None
    favourites = []

    if "username" in session:
        user = repository.get_user(session["username"])
        if user is not None:
            favourites = services.get_favourites_for_user(user=user,repository=repository,)

    return render_template("favourites/favourites.html",favourites=favourites, user=user)

@favourites_blueprint.post("/track/<int:track_id>/favourite")
@login_required
def add_favourite(track_id):
    repository = current_app.config["REPOSITORY"]
    user = repository.get_user(session["username"])
    services.add_favourite(user = user, track_id = track_id, repository = repository)
    return redirect(url_for("tracks.track_detail", track_id=track_id))

@favourites_blueprint.post("/track/<int:track_id>/favourite/remove")
@login_required
def remove_favourite(track_id):
    repository = current_app.config["REPOSITORY"]
    user = repository.get_user(session["username"])
    services.remove_favourite(user = user, track_id = track_id, repository = repository)
    return redirect(url_for("tracks.track_detail", track_id=track_id))