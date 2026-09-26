def test_user_can_search_and_open_track_details(client):
    # Step 1: The user searches for a track by title.
    search_response = client.get(
        "/search?query=Test+Track&criterion=title"
    )
    search_page = search_response.get_data(as_text=True)

    assert search_response.status_code == 200
    assert "Test Track" in search_page
    assert "Test Artist" in search_page
    assert 'href="/track/1"' in search_page

    # Step 2: The user opens the track from the search results.
    detail_response = client.get("/track/1")
    detail_page = detail_response.get_data(as_text=True)

    assert detail_response.status_code == 200
    assert "Test Track" in detail_page
    assert "Test Artist" in detail_page
    assert "Test Album" in detail_page
    assert "Test Genre" in detail_page
    assert "180" in detail_page