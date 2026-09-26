"""Tests for the Browse Tracks service, route, and repository boundary."""


from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.artist import Artist
from music.domainmodel.track import Track
from music.tracks.services import get_browse_page, get_tracks_for_browse


def make_track(track_id: int, title: str) -> Track:
    track = Track(track_id, title)
    track.artist = Artist(track_id, f"Artist {track_id}")
    return track


def test_browse_service_gets_all_tracks_sorts_titles_and_limits_to_20():
    repository = MemoryRepository()
    for index in range(25, 0, -1):
        repository.add_track(make_track(index, f"Track {index:02d}"))

    result = get_tracks_for_browse(repository)

    assert len(result) == 20
    assert [track.title for track in result] == [
        f"Track {index:02d}" for index in range(1, 21)
    ]


def test_browse_pagination_service_returns_consistent_pages():
    repository = MemoryRepository()
    for index in range(45, 0, -1):
        repository.add_track(make_track(index, f"Track {index:02d}"))

    first_page = get_browse_page(repository, requested_page=1)
    second_page = get_browse_page(repository, requested_page=2)
    third_page = get_browse_page(repository, requested_page=3)

    all_rendered_tracks = (
        first_page.tracks + second_page.tracks + third_page.tracks
    )

    assert first_page.current_page == 1
    assert first_page.total_pages == 3
    assert first_page.has_previous is False
    assert first_page.has_next is True
    assert len(first_page.tracks) == 20

    assert second_page.current_page == 2
    assert second_page.has_previous is True
    assert second_page.has_next is True
    assert len(second_page.tracks) == 20

    assert third_page.current_page == 3
    assert third_page.has_previous is True
    assert third_page.has_next is False
    assert len(third_page.tracks) == 5

    assert [track.title for track in all_rendered_tracks] == [
        f"Track {index:02d}" for index in range(1, 46)
    ]


def test_browse_pagination_service_handles_invalid_and_out_of_range_pages():
    repository = MemoryRepository()
    for index in range(25, 0, -1):
        repository.add_track(make_track(index, f"Track {index:02d}"))

    invalid_page = get_browse_page(repository, requested_page=-4)
    out_of_range_page = get_browse_page(repository, requested_page=999)

    assert invalid_page.current_page == 1
    assert invalid_page.tracks[0].title == "Track 01"

    assert out_of_range_page.current_page == 2
    assert [track.title for track in out_of_range_page.tracks] == [
        f"Track {index:02d}" for index in range(21, 26)
    ]

