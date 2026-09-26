from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.favourite import Favourite
from music.domainmodel.track import Track
from music.domainmodel.user import User


def test_repository_can_add_and_find_favourite():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    favourite = Favourite(1, user, track)

    repository.add_favourite(favourite)

    assert repository.get_favourite(user, track) == favourite
    assert repository.get_favourites_for_user(user) == [favourite]
    assert repository.get_number_of_favourites() == 1


def test_repository_can_remove_favourite():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    favourite = Favourite(1, user, track)

    repository.add_favourite(favourite)
    repository.remove_favourite(favourite)

    assert repository.get_favourite(user, track) is None
    assert repository.get_favourites_for_user(user) == []
    assert repository.get_number_of_favourites() == 0


def test_repository_does_not_duplicate_same_user_track_favourite():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")

    first_favourite = Favourite(1, user, track)
    duplicate_favourite = Favourite(2, user, track)

    repository.add_favourite(first_favourite)
    repository.add_favourite(duplicate_favourite)

    assert repository.get_number_of_favourites() == 1
    assert repository.get_favourite(user, track) == first_favourite