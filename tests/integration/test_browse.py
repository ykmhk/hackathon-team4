from music import MemoryRepository
from tests.unit.test_browse import make_track
from pathlib import Path
import re
from music import create_app

def test_browse_route_uses_configured_repository_and_jinja_loop():
    repository = MemoryRepository()
    repository.add_track(make_track(3, "Zulu"))
    repository.add_track(make_track(1, "alpha"))
    repository.add_track(make_track(2, "Bravo"))
    app = create_app({"TESTING": True, "REPOSITORY": repository})

    response = app.test_client().get("/browse")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert page.count('class="track-row"') == 3
    assert page.index("alpha") < page.index("Bravo") < page.index("Zulu")
    assert 'href="/browse"' in page
    assert "Page 1 of 1" in page


def test_browse_route_supports_page_query_and_navigation_links():
    repository = MemoryRepository()
    for index in range(25, 0, -1):
        repository.add_track(make_track(index, f"Track {index:02d}"))
    app = create_app({"TESTING": True, "REPOSITORY": repository})

    first_response = app.test_client().get("/browse?page=1")
    first_page = first_response.get_data(as_text=True)

    assert first_response.status_code == 200
    assert "Page 1 of 2" in first_page
    assert 'href="/browse?page=2"' in first_page
    assert "Track 01" in first_page
    assert "Track 21" not in first_page

    second_response = app.test_client().get("/browse?page=2")
    second_page = second_response.get_data(as_text=True)

    assert second_response.status_code == 200
    assert "Page 2 of 2" in second_page
    assert 'href="/browse?page=1"' in second_page
    assert "Track 01" not in second_page
    assert "Track 21" in second_page


def test_browse_route_handles_invalid_page_query_safely():
    repository = MemoryRepository()
    for index in range(25, 0, -1):
        repository.add_track(make_track(index, f"Track {index:02d}"))
    app = create_app({"TESTING": True, "REPOSITORY": repository})
    client = app.test_client()

    for invalid_value in ("not-a-number", "0", "-5"):
        response = client.get(f"/browse?page={invalid_value}")
        page = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "Page 1 of 2" in page
        assert "Track 01" in page

    response = client.get("/browse?page=999")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Page 2 of 2" in page
    assert "Track 21" in page


def test_browse_route_displays_first_20_real_csv_tracks_in_title_order():
    app = create_app({"TESTING": True})
    repository = app.config["REPOSITORY"]
    expected_tracks = sorted(
        repository.get_all_tracks(),
        key=lambda track: (track.title.casefold(), track.track_id),
    )[:20]

    response = app.test_client().get("/browse")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert page.count('class="track-row"') == 20

    rendered_track_ids = [
        int(track_id)
        for track_id in re.findall(r'data-track-id="(\d+)"', page)
    ]
    assert rendered_track_ids == [track.track_id for track in expected_tracks]


def test_browse_route_and_template_do_not_access_csv_files_directly():
    project_root = Path(__file__).resolve().parents[2]
    view_source = (project_root / "music" / "tracks" / "views.py").read_text(encoding="utf-8")
    template_source = (
        project_root / "music" / "templates" / "tracks" / "browse.html"
    ).read_text(encoding="utf-8")

    assert "CSVDataReader" not in view_source
    assert "open(" not in view_source
    assert ".csv" not in view_source
    assert "CSVDataReader" not in template_source
    assert ".csv" not in template_source
