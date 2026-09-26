"""Unit tests for review and rating service operations."""

import pytest

from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.reviews import services


def make_repository_with_track() -> tuple[MemoryRepository, Track]:
    repository = MemoryRepository()
    track = Track(1, "Test Track")
    repository.add_track(track)
    return repository, track


def test_add_review_updates_repository_and_user():
    repository, track = make_repository_with_track()
    user = User(1, "reviewer", "password123")

    review = services.add_review(user, track.track_id, 5, "Excellent track", repository)

    assert repository.get_reviews_for_track(track) == [review]
    assert review in user.reviews
    assert repository.get_number_of_reviews() == 1


def test_reviews_are_returned_newest_first_and_average_is_calculated():
    repository, track = make_repository_with_track()
    user = User(1, "reviewer", "password123")
    older_review = Review(1, user, track, 3, "Good", "2026-09-05 10:00:00")
    newer_review = Review(2, user, track, 5, "Excellent", "2026-09-05 11:00:00")
    repository.add_review(older_review)
    repository.add_review(newer_review)

    assert services.get_reviews_for_track(track.track_id, repository) == [newer_review, older_review]
    assert services.get_average_rating(track.track_id, repository) == 4.0


def test_average_rating_is_none_when_a_track_has_no_reviews():
    repository, track = make_repository_with_track()

    assert services.get_average_rating(track.track_id, repository) is None


def test_add_review_rejects_an_unknown_track():
    repository = MemoryRepository()
    user = User(1, "reviewer", "password123")

    with pytest.raises(ValueError, match="does not exist"):
        services.add_review(user, 999, 5, "Excellent", repository)
