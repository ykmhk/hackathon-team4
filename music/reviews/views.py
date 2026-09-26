"""HTTP routes for creating track reviews."""

from flask import abort, current_app, flash, redirect, render_template, session, url_for

from music.authentication.decorators import login_required
from music.reviews import reviews_blueprint, services
from music.reviews.forms import ReviewForm


def _render_track_detail_with_form(track, form, repository):
    """Render Track Detail with review data after an invalid POST submission."""
    user = repository.get_user(session["username"])
    is_favourite = repository.get_favourite(user, track) is not None

    return render_template(
        "tracks/track_detail.html",
        track=track,
        is_favourite=is_favourite,
        reviews=services.get_reviews_for_track(track.track_id, repository),
        average_rating=services.get_average_rating(track.track_id, repository),
        review_form=form,
    )


@reviews_blueprint.post("/track/<int:track_id>/review")
@login_required
def add_review(track_id):
    """Create a review for a Track, or redisplay field errors when invalid."""
    repository = current_app.config["REPOSITORY"]
    track = repository.get_track(track_id)
    if track is None:
        abort(404)

    form = ReviewForm()
    if not form.validate_on_submit():
        return _render_track_detail_with_form(track, form, repository), 400

    user = repository.get_user(session["username"])
    services.add_review(
        user=user,
        track_id=track_id,
        rating=form.rating.data,
        review_text=form.review_text.data.strip(),
        repository=repository,
    )
    flash("Review posted successfully.", "success")
    return redirect(url_for("tracks.track_detail", track_id=track_id))
