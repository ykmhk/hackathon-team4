import pytest
from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.favourite import Favourite
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.favourites import services


def test_add_favourite_updates_repository_and_user():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    repository.add_track(track)

    services.add_favourite(user, track.track_id, repository)

    favourite = repository.get_favourite(user, track)

    assert favourite is not None
    assert favourite in user.favourites
    assert repository.get_number_of_favourites() == 1


def test_add_favourite_does_not_create_duplicate():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    repository.add_track(track)

    first_favourite = services.add_favourite(
        user,
        track.track_id,
        repository,
    )
    second_favourite = services.add_favourite(
        user,
        track.track_id,
        repository,
    )

    assert second_favourite == first_favourite
    assert repository.get_number_of_favourites() == 1
    assert len(user.favourites) == 1


def test_remove_favourite_updates_repository_and_user():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    repository.add_track(track)

    services.add_favourite(user, track.track_id, repository)
    services.remove_favourite(user, track.track_id, repository)

    assert repository.get_favourite(user, track) is None
    assert repository.get_number_of_favourites() == 0
    assert user.favourites == []


def test_get_favourites_for_user():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    repository.add_track(track)

    services.add_favourite(user, track.track_id, repository)

    favourites = services.get_favourites_for_user(user, repository)

    assert len(favourites) == 1
    assert favourites[0].track == track


def test_add_favourite_rejects_unknown_track():
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")

    with pytest.raises(ValueError):
        services.add_favourite(user, 999, repository)


def test_is_favourite_returns_true_when_track_is_favourite(repository):
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    favourite = Favourite(1, user, track)
    repository.add_user(user)
    repository.add_track(track)
    repository.add_favourite(favourite)

    assert services.is_favourite("testuser",1,repository) is True

def test_is_favourite_returns_false_when_track_is_not_favourite(repository):
    repository = MemoryRepository()
    user = User(1, "testuser", "password123")
    track = Track(1, "Test Track")
    repository.add_user(user)
    repository.add_track(track)

    assert services.is_favourite("testuser",1,repository) is False