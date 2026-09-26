from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.track import Track
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.genre import Genre
from music.tracks.services import search_tracks, get_search_page

# Repository tests
def test_search_tracks_by_title():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track2 = Track(2, "Hello")
    repository.add_track(track1)
    repository.add_track(track2)

    result = repository.search_tracks("Feel Good", "title")
    assert result == [track1]


def test_search_tracks_by_artist():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track1.artist = Artist(1, "Gorillaz")
    track2 = Track(2, "Good Song")
    track2.artist = Artist(2, "Blur")
    repository.add_track(track1)
    repository.add_track(track2)

    result = repository.search_tracks("Gorillaz", "artist")
    assert result == [track1]


def test_search_tracks_ignores_tracks_without_artist():
    repository = MemoryRepository()
    track1 = Track(1, "Unknown Artist Song")
    track2 = Track(2, "Feel Good Inc.")
    track2.artist = Artist(2, "Gorillaz")
    repository.add_track(track1)
    repository.add_track(track2)

    result = repository.search_tracks("Gorillaz", "artist")
    assert result == [track2]


def test_search_tracks_by_artist_returns_all_matching_tracks():
    repository = MemoryRepository()

    track1 = Track(1, "Feel Good Inc.")
    track1.artist = Artist(1, "Gorillaz")
    track2 = Track(2, "Clint Eastwood")
    track2.artist = Artist(1, "Gorillaz")
    track3 = Track(3, "Song 2")
    track3.artist = Artist(2, "Blur")
    repository.add_track(track1)
    repository.add_track(track2)
    repository.add_track(track3)

    result = repository.search_tracks("Gorillaz", "artist")
    assert result == [track1, track2]


def test_search_tracks_by_album():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track1.album = Album(1, "Demon Days")
    track2 = Track(2, "Unknown Album Song")
    repository.add_track(track1)
    repository.add_track(track2)

    result = repository.search_tracks("Demon", "album")
    assert result == [track1]


def test_search_tracks_by_genre():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track1.add_genre(Genre(1, "Alternative Rock"))
    track2 = Track(2, "Song 2")
    track2.add_genre(Genre(2, "Rock"))
    repository.add_track(track1)
    repository.add_track(track2)

    result = repository.search_tracks("alternative", "genre")
    assert result == [track1]


def test_search_tracks_is_case_insensitive():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    track.artist = Artist(1, "Gorillaz")
    repository.add_track(track)

    result = repository.search_tracks("GoRiLLAz", "artist")
    assert result == [track]


def test_search_tracks_returns_empty_list_when_no_match():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    repository.add_track(track)

    result = repository.search_tracks("apple", "title")
    assert result == []





# Service tests
def test_search_service_returns_empty_for_blank_query():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    repository.add_track(track)

    result = search_tracks(" ", "title", repository)
    assert result == []

def test_search_service_rejects_invalid_criterion():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    repository.add_track(track)

    result = search_tracks("Feel Good", "invalid", repository)
    assert result == []

def test_search_service_returns_matching_tracks():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    repository.add_track(track)

    result = search_tracks("Feel Good", "title", repository)
    assert result == [track]

def test_get_search_page_returns_first_page():
    repository = MemoryRepository()

    for i in range(25):
        track = Track(i, f"Song {i}")
        repository.add_track(track)

    tracks, current_page, total_pages, has_previous, has_next = get_search_page(
        "Song", "title", repository,1)

    assert len(tracks) == 20
    assert current_page == 1
    assert total_pages == 2
    assert has_previous is False
    assert has_next is True

def test_get_search_page_returns_second_page():
    repository = MemoryRepository()

    for i in range(25):
        track = Track(i, f"Song {i}")
        repository.add_track(track)

    tracks, current_page, total_pages, has_previous, has_next = get_search_page(
        "Song", "title", repository,2)

    assert len(tracks) == 5
    assert current_page == 2
    assert total_pages == 2
    assert has_previous is True
    assert has_next is False

def test_get_search_page_returns_empty_for_no_results():
    repository = MemoryRepository()

    track = Track(1, "Hello")
    repository.add_track(track)

    tracks, current_page, total_pages, has_previous, has_next = get_search_page(
        "Apple", "title", repository,1)

    assert tracks == []
    assert current_page == 1
    assert total_pages == 1
    assert has_previous is False
    assert has_next is False


def test_get_search_page_clamps_page_to_last_page():
    repository = MemoryRepository()

    for i in range(25):
        track = Track(i, f"Song {i}")
        repository.add_track(track)

    tracks, current_page, total_pages, has_previous, has_next = get_search_page(
        "Song", "title", repository,999)

    assert current_page == 2
    assert total_pages == 2
    assert len(tracks) == 5
    assert has_previous is True
    assert has_next is False