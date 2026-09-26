"""HTTP routes for the tracks feature."""

from flask import Blueprint, current_app, render_template, request, session

from music.reviews import services as review_services
from music.reviews.forms import ReviewForm
from music.tracks import services
from music.favourites import services as favourite_services


tracks_blueprint = Blueprint("tracks", __name__)


@tracks_blueprint.get("/browse")
def browse():
    """Render a requested page of tracks supplied by the browse service."""
    repository = current_app.config["REPOSITORY"]

    requested_page = request.args.get("page", default=1, type=int)
    if requested_page is None:
        requested_page = 1

    browse_page = services.get_browse_page(repository, requested_page)

    return render_template(
        "tracks/browse.html",
        tracks=browse_page.tracks,
        current_page=browse_page.current_page,
        total_pages=browse_page.total_pages,
        has_previous=browse_page.has_previous,
        has_next=browse_page.has_next,
        per_page=services.TRACKS_PER_PAGE,
    )


@tracks_blueprint.get("/track/<int:track_id>")
def track_detail(track_id: int):
# Display details for a track.
    repository = current_app.config["REPOSITORY"]
    track = services.get_track(track_id, repository)
# Return `Track not found` with HTTP 404 for an unknown track ID.
    if track is None:
        return "Track not found", 404
    is_favourite = False
    if "username" in session:
        is_favourite = favourite_services.is_favourite(session["username"],track_id,repository)

    return render_template(
        "tracks/track_detail.html",
        track=track,
        is_favourite=is_favourite,
        reviews=review_services.get_reviews_for_track(track_id, repository),
        average_rating=review_services.get_average_rating(track_id, repository),
        review_form=ReviewForm(),
    )


@tracks_blueprint.get("/search")
def search():
    """Search for tracks using the selected criterion."""
    repository = current_app.config["REPOSITORY"]

    query = request.args.get("query", "").strip()
    criterion = request.args.get("criterion", "title")

    requested_page = request.args.get("page", default=1, type=int)

    if requested_page is None:
        requested_page = 1

    tracks, current_page, total_pages, has_previous, has_next = services.get_search_page(
        query,
        criterion,
        repository,
        requested_page,
    )

    return render_template(
        "tracks/search.html",
        tracks=tracks,
        query=query,
        criterion=criterion,
        current_page=current_page,
        total_pages=total_pages,
        has_previous=has_previous,
        has_next=has_next,
        per_page=services.TRACKS_PER_PAGE,
    )