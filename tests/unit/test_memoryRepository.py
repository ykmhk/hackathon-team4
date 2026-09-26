"""Tests for the in-memory Track repository and its CSV population.

These tests describe the small data-access contract taught in Lab 4.  They
exercise the repository directly, without Flask routes or HTML templates.
"""

from pathlib import Path

import pytest

from music.adapters.memory_repository import MemoryRepository
from music.adapters.repository_populate import populate_repository
from music.domainmodel.track import Track
from music import create_app
from music.domainmodel.user import User

# Keep population tests independent from the full application dataset. These
# fixtures are intentionally small, version-controlled, and designed for tests.
TEST_DATA_DIRECTORY = Path(__file__).resolve().parents[1] / 'data'
TEST_ALBUMS_FILE = TEST_DATA_DIRECTORY / 'raw_albums_test.csv'
TEST_TRACKS_FILE = TEST_DATA_DIRECTORY / 'raw_tracks_test.csv'


class TestMemoryRepository:
    """Check the concrete implementation of the AbstractRepository contract."""

    def test_add_track_and_get_track_by_id(self):
        """A stored Track can be retrieved later using its ID."""
        repository = MemoryRepository()
        track = Track(1, 'Example Track')

        repository.add_track(track)

        assert repository.get_track(1) == track

    def test_get_unknown_track_returns_none(self):
        """A missing ID is not an error at repository level; it returns None."""
        repository = MemoryRepository()

        assert repository.get_track(999) is None

    def test_get_all_tracks_returns_added_tracks(self):
        """The repository returns the Track objects that were added to it."""
        repository = MemoryRepository()
        first_track = Track(1, 'First Track')
        second_track = Track(2, 'Second Track')

        repository.add_track(first_track)
        repository.add_track(second_track)

        # The repository contract promises all stored Tracks, but does not
        # promise an ordering. Browse will sort explicitly in its service.
        assert set(repository.get_all_tracks()) == {first_track, second_track}


def test_populate_repository_loads_configured_csv_tracks():
    """Population loads the supplied test CSV files into a repository."""
    repository = MemoryRepository()

    populate_repository(
        repository,
        albums_file_path=TEST_ALBUMS_FILE,
        tracks_file_path=TEST_TRACKS_FILE,
    )

    # The test fixture has 10 Tracks, so this remains quick and deterministic.
    assert len(repository.get_all_tracks()) == 10

    track = repository.get_track(2)
    assert track is not None
    assert track.title == 'Food'


def test_populate_repository_rejects_only_one_csv_file():
    """Album and Track CSV files must be chosen as one matching pair."""
    repository = MemoryRepository()

    with pytest.raises(ValueError, match='both albums_file_path'):
        populate_repository(repository, albums_file_path=TEST_ALBUMS_FILE)

def test_create_app_configures_populated_repository():
    app = create_app({"TESTING": True})

    repository = app.config["REPOSITORY"]
    tracks = repository.get_all_tracks()

    assert isinstance(repository, MemoryRepository)
    assert len(tracks) == 2000

def test_create_app_keeps_an_injected_repository():
    repository = MemoryRepository()

    app = create_app({
        "TESTING": True,
        "REPOSITORY": repository,
    })

    assert app.config["REPOSITORY"] is repository

def test_add_user_and_get_user_by_username():
    """A stored User can be retrieved later using a case-insensitive username."""
    repository = MemoryRepository()
    user = User(1, "Meti", "Password1")

    repository.add_user(user)

    assert repository.get_user("meti") is user
    assert repository.get_user("  METI  ") is user

def test_get_unknown_user_returns_none():
    """Looking up a username that has not been stored returns None."""
    repository = MemoryRepository()

    assert repository.get_user("unknown-user") is None

def test_add_user_rejects_duplicate_username():
    """Two accounts must not be stored under the same normalized username."""
    repository = MemoryRepository()
    first_user = User(1, "Meti", "Password1")
    duplicate_user = User(2, "METI", "Password2")

    repository.add_user(first_user)

    with pytest.raises(ValueError, match="already exists"):
        repository.add_user(duplicate_user)

def test_get_number_of_users_counts_stored_users():
    """The repository provides the count needed to allocate the next User ID."""
    repository = MemoryRepository()

    assert repository.get_number_of_users() == 0

    repository.add_user(User(1, "Meti", "Password1"))

    assert repository.get_number_of_users() == 1