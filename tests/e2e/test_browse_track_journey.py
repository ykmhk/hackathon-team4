def test_user_can_browse_to_track_details_and_return(client):
    home_response = client.get("/")
    assert home_response.status_code == 200
    assert b'href="/browse"' in home_response.data

    browse_response = client.get("/browse")
    assert browse_response.status_code == 200
    browse_page = browse_response.get_data(as_text=True)
    assert "Test Track" in browse_page
    assert "Test Artist" in browse_page
    assert 'href="/track/1"' in browse_page

    detail_response = client.get("/track/1")
    assert detail_response.status_code == 200
    detail_page = detail_response.get_data(as_text=True)
    assert "Test Track" in detail_page
    assert "Test Artist" in detail_page
    assert "Test Album" in detail_page
    assert "Test Genre" in detail_page
    assert "180" in detail_page
    assert 'href="/browse"' in detail_page
    assert 'Back to Browse' in detail_page

    browse_again_response = client.get("/browse")
    assert browse_again_response.status_code == 200
    browse_again_page = browse_again_response.get_data(as_text=True)
    assert "Test Track" in browse_again_page
