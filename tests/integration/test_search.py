from music import create_app, MemoryRepository
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track


# Route / integration tests
def test_search_page_returns_200():
    app = create_app({"TESTING": True})
    response = app.test_client().get("/search")

    assert response.status_code == 200

def test_search_route_can_search_by_title():
    repository = MemoryRepository()
    track1 = Track(1, "Good Song")
    track2 = Track(2, "Hello")
    repository.add_track(track1)
    repository.add_track(track2)

    app = create_app({"TESTING": True,"REPOSITORY": repository})
    response = app.test_client().get( "/search?query=Good&criterion=title")

    assert response.status_code == 200
    assert b"Good Song" in response.data
    assert b"Hello" not in response.data


def test_search_route_can_search_by_artist():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track1.artist = Artist(1, "Gorillaz")
    track2 = Track(2, "Song 2")
    track2.artist = Artist(2, "Blur")
    repository.add_track(track1)
    repository.add_track(track2)

    app = create_app({ "TESTING": True,"REPOSITORY": repository})
    response = app.test_client().get("/search?query=Gorillaz&criterion=artist")

    assert response.status_code == 200
    assert b"Feel Good Inc." in response.data
    assert b"Song 2" not in response.data


def test_search_route_can_search_by_album():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track1.album = Album(1, "Demon Days")
    track2 = Track(2, "Song 2")
    track2.album = Album(2, "Blur")
    repository.add_track(track1)
    repository.add_track(track2)

    app = create_app({"TESTING": True,"REPOSITORY": repository,})
    response = app.test_client().get("/search?query=Demon&criterion=album")

    assert response.status_code == 200
    assert b"Feel Good Inc." in response.data
    assert b"Song 2" not in response.data


def test_search_route_can_search_by_genre():
    repository = MemoryRepository()
    track1 = Track(1, "Feel Good Inc.")
    track1.add_genre(Genre(1, "Alternative Rock"))
    track2 = Track(2, "Song 2")
    track2.add_genre(Genre(2, "Pop"))
    repository.add_track(track1)
    repository.add_track(track2)

    app = create_app({"TESTING": True,"REPOSITORY": repository,})
    response = app.test_client().get("/search?query=alternative&criterion=genre")

    assert response.status_code == 200
    assert b"Feel Good Inc." in response.data
    assert b"Song 2" not in response.data


def test_search_result_links_to_correct_track_detail():
    repository = MemoryRepository()
    track = Track(123, "Love Story")
    repository.add_track(track)

    app = create_app({"TESTING": True,"REPOSITORY": repository})
    response = app.test_client().get( "/search?query=love&criterion=title")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'href="/track/123"' in page


def test_search_route_displays_message_when_no_tracks_match():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    repository.add_track(track)

    app = create_app({"TESTING": True,"REPOSITORY": repository})
    response = app.test_client().get("/search?query=apple&criterion=title")

    assert response.status_code == 200
    assert b"No tracks found" in response.data

def test_track_detail_displays_track_information():
    repository = MemoryRepository()
    track = Track(1, "Feel Good Inc.")
    track.artist = Artist(1, "Gorillaz")
    track.album = Album(1, "Demon Days")
    track.album.release_year = 2005
    track.track_duration = 222
    track.add_genre(Genre(1, "Alternative Rock"))
    track.add_genre(Genre(2, "Alternative"))
    repository.add_track(track)

    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "REPOSITORY": repository,
    })
    response = app.test_client().get("/track/1")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Feel Good Inc." in page
    assert "Gorillaz" in page
    assert "Demon Days" in page
    assert "2005" in page
    assert "222" in page
    assert "Alternative Rock" in page
    assert "Alternative" in page


def test_navbar_contains_search_form():
    repository = MemoryRepository()
    app = create_app({"TESTING": True,"REPOSITORY": repository})
    response = app.test_client().get("/browse")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert '<form class="nav-search"' in page
    assert 'action="/search"' in page
    assert 'name="query"' in page
    assert 'name="criterion"' in page
