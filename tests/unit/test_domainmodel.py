import pytest
import os

from music.domainmodel.artist import Artist
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.album import Album
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User
from music.adapters.csvdatareader import CSVDataReader


class TestArtist:

    def test_construction(self):
        artist1 = Artist(1, 'Tailor Swift')
        assert str(artist1) == "<Artist Tailor Swift, artist id = 1>"
        artist2 = Artist(2, "Maroon 5")
        assert str(artist2) == '<Artist Maroon 5, artist id = 2>'
        artist3 = Artist(3, 'Kate Bush')
        assert str(artist3) == '<Artist Kate Bush, artist id = 3>'

        # Test full_name with trailing spaces
        artist4 = Artist(4, ' Bad Bunny ')
        assert str(artist4) == '<Artist Bad Bunny, artist id = 4>'

        # Test when the id is None
        with pytest.raises(ValueError):
            Artist(None, 'Harry Styles')

        # Test when the id is negative
        with pytest.raises(ValueError):
            Artist(-3, 'Harry Styles')

        # full_name is a required field -> invalid type raises, not None
        with pytest.raises(ValueError):
            Artist(5, 2910)

    def test_setters(self):
        artist1 = Artist(1, 'Tailor Swift')

        # Test full_name setter
        artist1.full_name = '  Tailor Fixed  '
        assert artist1.full_name == 'Tailor Fixed'
        assert str(artist1) == '<Artist Tailor Fixed, artist id = 1>'

        # full_name is required -> invalid type raises
        with pytest.raises(ValueError):
            artist1.full_name = 32
        assert artist1.full_name == 'Tailor Fixed'

        with pytest.raises(ValueError):
            artist1.full_name = '   '
        assert artist1.full_name == 'Tailor Fixed'

    def test_equality(self):
        artist1 = Artist(1, 'Tailor Swift')
        artist2 = Artist(2, "Maroon 5")
        artist3 = Artist(3, 'Kate Bush')
        artist3_copy = Artist(3, 'Kate Bush')

        # Check equality of the same artists
        assert artist1 == artist1
        assert artist2 == artist2
        assert artist3 == artist3
        assert artist3 == artist3_copy

        # Check inequality of different artists
        assert artist1 != artist2
        assert artist1 != artist3
        assert artist2 != artist3

        # Check equality with different types
        assert artist1 != 'Tailor Swift'
        assert artist1 is not None

    def test_sorting(self):
        artist1 = Artist(2, 'Tailor Swift')
        artist2 = Artist(5, "Maroon 5")
        artist3 = Artist(8, 'Kate Bush')

        # Basic inequality comparison
        assert artist1 < artist2
        assert artist2 < artist3
        assert artist3 > artist1

        # Test actual sorting of the list of artists
        artist_list = [artist3, artist2, artist1]
        assert sorted(artist_list) == [artist1, artist2, artist3]

    def test_set(self):
        artist1 = Artist(1, 'Tailor Swift')
        artist2 = Artist(3, "Maroon 5")
        artist3 = Artist(8, 'Kate Bush')

        artist_set = set()
        # Test addition
        artist_set.add(artist1)
        artist_set.add(artist2)
        artist_set.add(artist3)

        assert sorted(artist_set) == [artist1, artist2, artist3]

        # Test removal
        artist_set.discard(artist1)
        assert sorted(artist_set) == [artist2, artist3]


class TestGenre:

    def test_construction(self):
        genre1 = Genre(1, 'Jazz ')
        genre2 = Genre(2, ' Electronic ')

        assert str(genre1) == '<Genre Jazz, genre id = 1>'
        assert str(genre2) == '<Genre Electronic, genre id = 2>'

        # Test invalid id raises error
        with pytest.raises(ValueError):
            Genre('abc', 'Chill')

        # Test invalid id raises error
        with pytest.raises(ValueError):
            Genre(-30, 'Chill')

        # name is a required field -> invalid type raises
        with pytest.raises(ValueError):
            Genre(3, 300)

    def test_setters(self):
        genre1 = Genre(1, 'Jazz')

        assert genre1.genre_id == 1

        genre1.name = 'New Jazz'
        assert genre1.name == 'New Jazz'

        # Invalid type assignment raises and leaves the value untouched
        with pytest.raises(ValueError):
            genre1.name = 100
        assert genre1.name == 'New Jazz'

        # Empty string assignment raises and leaves the value untouched
        with pytest.raises(ValueError):
            genre1.name = ''
        assert genre1.name == 'New Jazz'

    def test_equality(self):
        genre1 = Genre(1, 'Jazz')
        genre2 = Genre(2, 'Electronic')
        genre3 = Genre(5, 'Electronic')

        assert genre1 == genre1
        assert genre1 != genre2
        assert genre2 != genre3

        assert genre1 != 'Jazz'
        assert genre2 != 105

    def test_sorting(self):
        genre1 = Genre(1, 'Jazz')
        genre2 = Genre(2, 'Electronic')
        genre3 = Genre(8, 'Latin')

        assert genre1 < genre2
        assert genre2 < genre3
        assert genre3 > genre1

        genre_list = [genre3, genre2, genre1]
        assert sorted(genre_list) == [genre1, genre2, genre3]

    def test_set(self):
        genre1 = Genre(1, 'Jazz')
        genre2 = Genre(2, 'Electronic')
        genre3 = Genre(8, 'Latin')

        genre_set = set()
        genre_set.add(genre1)
        genre_set.add(genre2)
        genre_set.add(genre3)

        assert sorted(genre_set) == [genre1, genre2, genre3]

        genre_set.discard(genre2)
        genre_set.discard(genre1)
        assert sorted(genre_set) == [genre3]


class TestAlbum:

    def test_construction(self):
        album = Album(1, '  AWOL - A Way Of Life  ')

        assert album.album_id == 1
        assert album.title == 'AWOL - A Way Of Life'
        assert album.release_year is None
        assert album.total_tracks is None
        assert album.album_url is None
        assert album.album_type is None
        # assert album.album_image is None
        assert str(album) == '<Album AWOL - A Way Of Life, album id = 1>'

        with pytest.raises(ValueError):
            Album(None, 'AWOL - A Way Of Life')
        with pytest.raises(ValueError):
            Album(-1, 'AWOL - A Way Of Life')
        with pytest.raises(ValueError):
            Album(1, '   ')
        with pytest.raises(ValueError):
            Album(1, 2009)

    def test_setters(self):
        album = Album(1, 'AWOL - A Way Of Life')

        album.title = '  New title  '
        album.release_year = 2009
        album.total_tracks = 7
        album.album_url = '  https://example.com/album  '
        album.album_type = '  Album  '
        # album.album_image = '  https://example.com/cover.jpg  '

        assert album.title == 'New title'
        assert album.release_year == 2009
        assert album.total_tracks == 7
        assert album.album_url == 'https://example.com/album'
        assert album.album_type == 'Album'
        # assert album.album_image == 'https://example.com/cover.jpg'

        with pytest.raises(ValueError):
            album.title = ''
        with pytest.raises(ValueError):
            album.release_year = -1
        with pytest.raises(ValueError):
            album.total_tracks = '7'
        with pytest.raises(ValueError):
            album.album_url = '   '
        with pytest.raises(ValueError):
            album.album_type = 1
        # with pytest.raises(ValueError):
        #     album.album_image = ''

        assert album.title == 'New title'
        assert album.release_year == 2009
        assert album.total_tracks == 7
        assert album.album_url == 'https://example.com/album'
        assert album.album_type == 'Album'
        # assert album.album_image == 'https://example.com/cover.jpg'

        album.release_year = None
        album.total_tracks = None
        album.album_url = None
        album.album_type = None
        # album.album_image = None

        assert album.release_year is None
        assert album.total_tracks is None
        assert album.album_url is None
        assert album.album_type is None
        # assert album.album_image is None

    def test_equality_sorting_and_set(self):
        album1 = Album(1, 'AWOL - A Way Of Life')
        album1_copy = Album(1, 'Different title, same identity')
        album2 = Album(4, 'Niris')
        album3 = Album(6, 'Constant Hitmaker')

        assert album1 == album1_copy
        assert album1 != album2
        assert album1 != 'AWOL - A Way Of Life'
        assert sorted([album3, album1, album2]) == [album1, album2, album3]
        assert len({album1, album1_copy, album2, album3}) == 3

    #
    # def test_album_image_can_be_set(self):
    #     album = Album(1, "Test Album")
    #     album.album_image = "https://example.com/cover.jpg"
    #
    #     assert album.album_image == "https://example.com/cover.jpg"
    #
    # def test_album_image_can_be_none(self):
    #     album = Album(1, "Test Album")
    #     album.album_image = None
    #
    #     assert album.album_image is None
    #
    # def test_album_image_rejects_empty_string(self):
    #     album = Album(1, "Test Album")
    #
    #     with pytest.raises(ValueError):
    #         album.album_image = ""
    #
    #     assert album.album_image is None



class TestTrack:

    def test_construction(self):
        track1 = Track(1, 'As it Was ')
        track2 = Track(2, ' Heat Waves')
        track3 = Track(3, ' Tarot ')

        assert str(track1) == '<Track As it Was, track id = 1>'
        assert str(track2) == '<Track Heat Waves, track id = 2>'
        assert str(track3) == '<Track Tarot, track id = 3>'

        # Test if id of wrong type raises error
        with pytest.raises(ValueError):
            Track(None, 'Te Felicito')

        # Test negative value of id raises error
        with pytest.raises(ValueError):
            Track(-1, 'Te Felicito')

        # title is a required field -> invalid type raises, not None
        with pytest.raises(ValueError):
            Track(5, 32)

    def test_attributes(self):
        track1 = Track(1, 'Shivers')

        # Test title setter
        track1.title = 'Fixed Shivers'
        assert track1.title == 'Fixed Shivers'

        # Title with trailing spaces
        track1.title = '  Fixed Shivers2   '
        assert track1.title == 'Fixed Shivers2'

        # Test track_url
        track1.track_url = ' https://spotify/track/1 '
        assert track1.track_url == 'https://spotify/track/1'

        # track_url is optional -> None is a valid value
        track1.track_url = None
        assert track1.track_url is None

        # Test track duration
        track1.track_duration = 300
        assert track1.track_duration == 300

        # track_duration is optional -> None is a valid value
        track1.track_duration = None
        assert track1.track_duration is None

        artist = Artist(31, 'Justin Bieber')
        # Test artist attribute
        track1.artist = artist
        assert track1.artist == artist

        # artist is optional -> None is a valid value
        track1.artist = None
        assert track1.artist is None

    def test_attributes_fail(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(2, 'Heat Waves')

        with pytest.raises(ValueError):
            track1.track_url = 23
        assert track1.track_url is None

        # title is required -> invalid type raises
        with pytest.raises(ValueError):
            track1.title = 1256
        assert track1.title == 'Shivers'

        with pytest.raises(ValueError):
            track1.title = ''
        assert track1.title == 'Shivers'

        with pytest.raises(ValueError):
            track1.track_duration = '300 seconds'

        with pytest.raises(ValueError):
            track2.track_duration = -20

        assert track1.track_duration is None
        assert track2.track_duration is None

        # Assigning artist of invalid type raises; value stays None
        with pytest.raises(ValueError):
            track1.artist = 3235
        with pytest.raises(ValueError):
            track2.artist = 'invalid artist'
        assert track1.artist is None
        assert track2.artist is None

        # Assigning album of invalid type raises; value stays None
        with pytest.raises(ValueError):
            track1.album = 1983
        with pytest.raises(ValueError):
            track2.album = 'Invalid album'
        assert track1.album is None
        assert track2.album is None

    def test_genre_methods(self):
        track1 = Track(1, 'Shivers')
        genre1 = Genre(10, 'Jazz')
        genre2 = Genre(11, 'Clasical')

        track1.add_genre(genre1)
        track1.add_genre(genre2)
        assert track1.genres == [genre1, genre2]

        # Should do nothing
        track1.add_genre('32')
        assert track1.genres == [genre1, genre2]

    def test_equality(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(2, 'Heat Waves')
        track3 = Track(3, 'Bad Habit')

        assert track1 == track1
        assert track2 == track2
        assert track1 != track2
        assert track1 != track3

        assert track2 != 30
        assert track3 != 'Bad Habit'

    def test_sorting(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(8, 'Heat Waves')
        track3 = Track(10, 'Bad Habit')

        assert track1 < track2
        assert track2 < track3
        assert track3 > track1

        track_list = [track3, track1, track2, track1]
        assert sorted(track_list) == [track1, track1, track2, track3]

    def test_set(self):
        track1 = Track(1, 'Shivers')
        track2 = Track(8, 'Heat Waves')
        track3 = Track(10, 'Bad Habit')

        track_set = set()
        track_set.add(track1)
        track_set.add(track2)
        track_set.add(track3)

        assert len(track_set) == 3

        track_set.discard(track1)
        assert sorted(track_set) == [track2, track3]

        track_set.discard(track2)
        track_set.discard(track3)
        assert len(track_set) == 0


class TestUser:

    def test_construction(self):
        user1 = User(7231, 'amotys', 'amotys277')
        user2 = User(9137, '  yunwi5  ', 'urrabbit978')

        assert str(user1) == '<User amotys, user id = 7231>'
        assert str(user2) == '<User yunwi5, user id = 9137>'

        # Invalid ID type raises error
        with pytest.raises(ValueError):
            User('invalid id', 'pedri', 'pedri1928')

        # ID less than 0 raises error
        with pytest.raises(ValueError):
            User(-10, 'peri', 'pedri1928')

        # Test user_name is all lowercase
        user3 = User(3829, ' GAVI ', 'gavi1928')
        assert user3.user_name == 'gavi'

        # user_name is required -> invalid type raises
        with pytest.raises(ValueError):
            User(8190, 1259, 'memphis212')

        # password is required -> invalid type raises
        with pytest.raises(ValueError):
            User(6737, 'Memphis', 325)

        # password is required -> empty string raises
        with pytest.raises(ValueError):
            User(9821, 'Memphis', '')

        # password length < 7 raises
        with pytest.raises(ValueError):
            User(6878, 'memphis', 'mempi')

        # Password of length 7 constructs correctly
        user6 = User(2918, 'Memphis', 'mempi12')
        assert user6.password == 'mempi12'

    # User class has getters for each attribute, but no setters.
    def test_attributes(self):
        user1 = User(7231, '  AMOTYS  ', 'amotys277')
        assert user1.user_id == 7231
        assert user1.user_name == 'amotys'
        assert user1.password == 'amotys277'

    def test_attributes_fail(self):
        user1 = User(7231, '  LEOROSE  ', 'LEOROSE277')

        with pytest.raises(AttributeError):
            user1.user_name = 'changed'

        with pytest.raises(AttributeError):
            user1.user_id = 1232

        with pytest.raises(AttributeError):
            user1.password = 'asdfe'

    def test_equality(self):
        user1 = User(2231, 'amotys', 'amotys277')
        user1_copy = User(2231, 'amotys', 'amotys277')
        user2 = User(7232, 'gavi', 'gavi9281')
        user3 = User(9300, 'phil', 'phi8901')

        assert user1 == user1_copy
        assert user1 != user2
        assert user2 != user3

        # Check equality with different types
        track1 = Track(2231, 'Chill with me')
        assert user1 != track1
        assert user1 != 'some user'
        assert user2 != 7120
        assert user3 is not None

    def test_sorting(self):
        user1 = User(2231, 'amotys', 'amotys277')
        user2 = User(7232, 'gavi', 'gavi9281')
        user3 = User(9300, 'phil', 'phi8901')

        assert user1 < user2
        assert user2 < user3
        assert user3 > user1

        user_list = [user3, user2, user1, user2]
        assert sorted(user_list) == [user1, user2, user2, user3]

    def test_set(self):
        user1 = User(2231, 'amotys', 'amotys277')
        user2 = User(7232, 'gavi', 'gavi9281')
        user3 = User(9300, 'phil', 'phi8901')

        user_set = set()
        user_set.add(user1)
        user_set.add(user2)
        user_set.add(user3)

        # Test all users were added to the set
        assert sorted(user_set) == [user1, user2, user3]

        # Test users are successfully removed from the set.
        user_set.discard(user1)
        user_set.discard(user2)
        assert list(user_set) == [user3]

class TestFavourite:

    def test_construction(self):
        user = User(1, 'amotys', 'amotys277')
        track = Track(10, 'Chill with me')
        favourite = Favourite(1, user, track)
        # checking attributes and string representation
        assert favourite.favourite_id == 1
        assert favourite.user == user
        assert favourite.track == track
        assert str(favourite) == '<Favourite 1, User: amotys, Track: Chill with me>'

        # wrong id
        with pytest.raises(ValueError):
            Favourite(None, user, track)
        with pytest.raises(ValueError):
            Favourite(-1, user, track)
        with pytest.raises(ValueError):
            Favourite('1', user, track)

        # wrong user value
        with pytest.raises(ValueError):
            Favourite(1, None, track)
        with pytest.raises(ValueError):
            Favourite(1, 'invalid_user', track)

        # wrong track value
        with pytest.raises(ValueError):
            Favourite(1, user, None)
        with pytest.raises(ValueError):
            Favourite(1, user, 'invalid_track')

    # suppose to be without setter so no change of attributes can be made
    def test_attributes_read_only(self):
        user = User(1, 'alice', 'password123')
        track = Track(1, 'Test Song')
        favourite = Favourite(1, user, track)

        with pytest.raises(AttributeError):
            favourite.favourite_id = 2
        with pytest.raises(AttributeError):
            favourite.user = None
        with pytest.raises(AttributeError):
            favourite.track = None

    def test_equality(self):
        user1 = User(1, 'alice', 'password123')
        user2 = User(2, 'bob', 'password456')
        track1 = Track(101, 'Song A')
        track2 = Track(102, 'Song B')

        fav1 = Favourite(1, user1, track1)
        fav1_same_id = Favourite(1, user2, track2)
        fav2 = Favourite(2, user1, track2)

        #equal only when same id
        assert fav1 == fav1_same_id
        assert fav1 != fav2
        assert fav1 != "None Favourite object"

    def test_sorting_and_set(self):
        user = User(1, 'alice', 'password123')
        track = Track(101, 'Song A')

        fav1 = Favourite(1, user, track)
        fav2 = Favourite(2, user, track)
        fav3 = Favourite(3, user, track)

        # test __lt__
        assert fav1 < fav2
        assert sorted([fav3, fav1, fav2]) == [fav1, fav2, fav3]

        # test __hash__ and __eq__
        fav_set = {fav1, fav2, fav3, fav1}
        assert len(fav_set) == 3
        assert fav1 in fav_set



def create_csv_reader():
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # # Test dataset location
    # albums_file_name = os.path.join(dirname, 'data/raw_albums_test.csv')
    # tracks_file_name = os.path.join(dirname, 'data/raw_tracks_test.csv')

    # Real dataset location
    albums_file_name = os.path.join(dirname, '../music/adapters/data/raw_albums_excerpt.csv')
    tracks_file_name = os.path.join(dirname, '../music/adapters/data/raw_tracks_excerpt.csv')

    reader = CSVDataReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()
    return reader


class TestCSVDataReader:

    def test_csv_reader(self):
        reader = create_csv_reader()

        assert len(reader.dataset_of_tracks) == 2000
        assert len(reader.dataset_of_artists) == 263
        assert len(reader.dataset_of_albums) == 427
        assert len(reader.dataset_of_genres) == 60

    def test_tracks_dataset(self):
        reader = create_csv_reader()
        tracks = reader.dataset_of_tracks

        sorted_tracks = sorted(tracks)
        # Test there are total 10 unique tracks in the test dataset // 2000 in real dataset.
        assert len(sorted_tracks) == 2000

        sorted_tracks_str = str(sorted_tracks[:3])
        assert sorted_tracks_str == '[<Track Food, track id = 2>, <Track Electric Ave, track id = 3>, <Track This World, track id = 5>]'

        # Test all tracks have artists
        tracks_no_artists = list(
            filter(lambda track: track.artist is None, tracks))
        assert len(tracks_no_artists) == 0

    def test_albums_dataset(self):
        reader = create_csv_reader()
        albums_set = reader.dataset_of_albums
        sorted_albums = sorted(albums_set)

        # Test there are total 5 unique albums in the test dataset // 427 in real dataset.
        assert len(sorted_albums) == 427

        sorted_albums_sample = str(sorted_albums[:3])
        assert sorted_albums_sample == '[<Album AWOL - A Way Of Life, album id = 1>, <Album Niris, album id = 4>, <Album Constant Hitmaker, album id = 6>]'

    def test_artists_dataset(self):
        reader = create_csv_reader()
        artists_set = reader.dataset_of_artists
        sorted_artists = sorted(artists_set)

        # Test there are total 5 unique artists in the test dataset // 263 in real dataset.
        assert len(sorted_artists) == 263

        sorted_artists_sample = str(sorted_artists[:3])
        assert sorted_artists_sample == '[<Artist AWOL, artist id = 1>, <Artist Nicky Cook, artist id = 4>, <Artist Kurt Vile, artist id = 6>]'

    def test_genres_dataset(self):
        reader = create_csv_reader()
        genres_set = reader.dataset_of_genres

        sorted_genres = sorted(genres_set)

        # Test there are total 7 unique genres in the test dataset // 60 in real dataset.
        assert len(sorted_genres) == 60

        sorted_genre_sample = str(sorted_genres[:3])
        assert sorted_genre_sample == '[<Genre Avant-Garde, genre id = 1>, <Genre International, genre id = 2>, <Genre Blues, genre id = 3>]'

    # def test_albums_load_album_images(self):
    #     reader = create_csv_reader()
    #     has_image = False
    #
    #     for album in reader.dataset_of_albums:
    #         if album.album_image is not None:
    #             has_image = True
    #             break
    #
    #     assert has_image


class TestReview:
    def test_review_object(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        review = Review(1, user, track, 5, "So Nice", "2026-08-13")
        assert review.review_id == 1
        assert review.user == user
        assert review.track == track
        assert review.rating == 5
        assert review.review_text == "So Nice"
        assert review.date == "2026-08-13"
        assert str(review) == "<Review 1, rating = 5>"

    def test_invalid_review_id(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        with pytest.raises(ValueError):
            Review(-1, user, track, 5, "So Nice", "2026-08-13")
        with pytest.raises(ValueError):
            Review(None, user, track, 5, "So Nice", "2026-08-13")
        with pytest.raises(ValueError):
            Review("one", user, track, 5, "So Nice", "2026-08-13")

    def test_invalid_rating(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        with pytest.raises(ValueError):
            Review(1, user, track, 6, "So Nice", "2026-08-13")
        with pytest.raises(ValueError):
            Review(1, user, track, -1, "So Nice", "2026-08-13")
        with pytest.raises(ValueError):
            Review(1, user, track, None, "So Nice", "2026-08-13")

    def test_invalid_review_text(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        with pytest.raises(ValueError):
            Review(1, user, track, 5, "", "2026-08-13")
        with pytest.raises(ValueError):
            Review(1, user, track, 5, "  ", "2026-08-13")
        with pytest.raises(ValueError):
            Review(1, user, track, 5, None, "2026-08-13")

    def test_equality(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        review1 = Review(1, user, track, 5, "So Nice", "2026-08-13")
        review1_copy = Review(1, user, track, 4, "Not Bad", "2026-08-14")
        review2 = Review(2, user, track, 5, "So Nice", "2026-08-13")
        assert review1 == review1_copy
        assert review1 != review2
        assert review1 != "Review"

    def test_sorting(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        review1 = Review(1, user, track, 5, "So Nice", "2026-08-13")
        review2 = Review(2, user, track, 4, "So Nice", "2026-08-13")
        review3 = Review(3, user, track, 3, "So Nice", "2026-08-13")
        assert review1 < review2
        assert review2 < review3
        assert sorted([review3, review1, review2]) == [review1, review2, review3]

    def test_set(self):
        user = User(1,"Example User", "ExamplePassword")
        track = Track(1, "Example Track")
        review1 = Review(1, user, track, 5, "So Nice", "2026-08-13")
        review1_copy = Review(1, user, track, 4, "Not Bad", "2026-08-14")
        review2 = Review(2, user, track, 5, "So Nice", "2026-08-13")
        review_set = {review1, review1_copy, review2}
        assert len(review_set) == 2