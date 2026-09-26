from music import create_app, MemoryRepository
from music.domainmodel.track import Track


# route successfully return detail
def test_track_detail_route_returns_200():
    repository = MemoryRepository()
    track = Track(1, "Example Track")
    repository.add_track(track)

    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "REPOSITORY": repository,
    })

    response = app.test_client().get("/track/1")

    assert response.status_code == 200
    assert b"Example Track" in response.data

# if track unknown should return 404
def test_track_detail_route_returns_404_for_unknown_track():
    repository = MemoryRepository()

    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "REPOSITORY": repository,
    })

    response = app.test_client().get("/track/999")

    assert response.status_code == 404
    assert b"Track not found" in response.data


#  page can links back to Browse
def test_track_detail_page_contains_back_to_browse_link():
    repository = MemoryRepository()
    track = Track(1, "Example Track")
    repository.add_track(track)

    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "REPOSITORY": repository,
    })

    response = app.test_client().get("/track/1")

    assert response.status_code == 200
    assert b"Back to Browse" in response.data
