from music.domainmodel.artist import Artist
from music.domainmodel.track import Track


def test_user_can_move_between_browse_pages(client, repository):
    # Arrange: Add enough tracks to require two browse pages.
    for track_id in range(2, 27):
        track = Track(track_id, f"Pagination Track {track_id:02d}")
        track.artist = Artist(track_id, f"Artist {track_id:02d}")
        repository.add_track(track)

    # Step 1: The user opens the first browse page.
    first_response = client.get("/browse?page=1")
    first_page = first_response.get_data(as_text=True)

    assert first_response.status_code == 200
    assert "Pagination Track 02" in first_page
    assert "Pagination Track 22" not in first_page
    assert 'href="/browse?page=2"' in first_page

    # Step 2: The user moves to the second browse page.
    second_response = client.get("/browse?page=2")
    second_page = second_response.get_data(as_text=True)

    assert second_response.status_code == 200
    assert "Pagination Track 22" in second_page
    assert "Pagination Track 02" not in second_page
    assert 'href="/browse?page=1"' in second_page