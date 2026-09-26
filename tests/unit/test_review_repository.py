"""Unit tests for review storage in MemoryRepository."""

from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


def test_repository_stores_reviews_for_their_track():
    repository = MemoryRepository()
    user = User(1, "reviewer", "password123")
    first_track = Track(1, "First Track")
    second_track = Track(2, "Second Track")
    first_review = Review(1, user, first_track, 5, "Excellent", "2026-09-05 10:00:00")
    second_review = Review(2, user, second_track, 3, "Good", "2026-09-05 10:01:00")

    repository.add_review(first_review)
    repository.add_review(second_review)

    assert repository.get_reviews_for_track(first_track) == [first_review]
    assert repository.get_reviews_for_track(second_track) == [second_review]
    assert repository.get_number_of_reviews() == 2
