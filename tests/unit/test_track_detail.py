from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Track
from music.tracks.services import get_track


# test if service can find track
def test_get_track_returns_track():
    repository = MemoryRepository()
    track = Track(1, "Example Track")
    repository.add_track(track)
    result = get_track(1, repository)
    assert result == track

# if track not exist return none
def test_get_track_returns_none_for_unknown_id():
    repository = MemoryRepository()

    result = get_track(999, repository)

    assert result is None
