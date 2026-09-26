"""Shared pytest fixtures for Music Library web-application tests."""

import pytest

from music import create_app
from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track


@pytest.fixture
def repository():
    """Return an isolated repository containing one predictable test track."""
    repo = MemoryRepository()
    track = Track(1, "Test Track")
    track.artist = Artist(1, "Test Artist")
    track.album = Album(1, "Test Album")
    track.add_genre(Genre(1, "Test Genre"))
    track.track_duration = 180
    track.track_url = "https://example.com/test-track"
    repo.add_track(track)
    return repo


@pytest.fixture
def app(repository):
    """Create an isolated test app with authentication test settings."""
    return create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret-key",
            "WTF_CSRF_SECRET_KEY": "test-csrf-secret-key",
            "REPOSITORY": repository,
        }
    )


@pytest.fixture
def client(app):
    """Return a Flask test client for the isolated test application."""
    return app.test_client()