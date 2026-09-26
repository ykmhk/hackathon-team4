"""Business operations for track reviews and ratings."""

from datetime import datetime

from music.adapters.repository import AbstractRepository
from music.domainmodel.review import Review
from music.domainmodel.user import User


def add_review(
        user: User,
        track_id: int,
        rating: int,
        review_text: str,
        repository: AbstractRepository,
) -> Review:
    """Create and store a Review for an existing Track."""
    track = repository.get_track(track_id)
    if track is None:
        raise ValueError(f"Track with ID {track_id} does not exist.")

    review = Review(
        review_id=repository.get_number_of_reviews() + 1,
        user=user,
        track=track,
        rating=rating,
        review_text=review_text,
        date=datetime.now().isoformat(timespec="microseconds"),
    )
    repository.add_review(review)
    user.add_review(review)
    return review


def get_reviews_for_track(
        track_id: int,
        repository: AbstractRepository,
) -> list[Review]:
    """Return a Track's Reviews with the newest submission first."""
    track = repository.get_track(track_id)
    if track is None:
        raise ValueError(f"Track with ID {track_id} does not exist.")

    return sorted(
        repository.get_reviews_for_track(track),
        key=lambda review: review.date,
        reverse=True,
    )


def get_average_rating(
        track_id: int,
        repository: AbstractRepository,
) -> float | None:
    """Return a one-decimal average rating, or None when there are no Reviews."""
    reviews = get_reviews_for_track(track_id, repository)
    if not reviews:
        return None

    return round(sum(review.rating for review in reviews) / len(reviews), 1)
