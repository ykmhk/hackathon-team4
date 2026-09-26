import os
import csv
import ast

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre


class CSVDataReader:
    def __init__(self,albums_file_name:str,tracks_file_name:str):
        self.albums_file_name=albums_file_name
        self.tracks_file_name=tracks_file_name

        self.dataset_of_tracks = set()
        self.dataset_of_genres = set()
        self.dataset_of_albums = set()
        self.dataset_of_artists = set()

    def read_csv_files(self):

        # Rebuild all datasets by reading the album and track CSV files.
        self.dataset_of_tracks = set()
        self.dataset_of_genres = set()
        self.dataset_of_albums = set()
        self.dataset_of_artists = set()

        albums_by_id = self.__read_albums()
        genres_by_id = {}
        artists_by_id = {}

        self.__read_tracks(albums_by_id,artists_by_id,genres_by_id)


    def __read_albums(self)->dict[int,Album]:
        albums_by_id = {}
        # The supplied CSV files contain Windows-1252 characters, so UTF-8 would fail.
        with open(self.albums_file_name,encoding='cp1252',newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                album_id = int(row['album_id'])
                if album_id in albums_by_id:
                    continue

                album=Album(album_id,row['album_title'])

                album.release_year = self.__optional_int(row['album_year_released'])
                album.total_tracks = self.__optional_int(row['album_tracks'])
                album.album_type = self.__optional_text(row['album_type']  )
                album.album_url = self.__optional_text(row['album_url'])
                # album.album_image = self.__optional_text(row['album_image_file'])

                albums_by_id[album_id] = album
                self.dataset_of_albums.add(album)
        return albums_by_id

    def __read_tracks(
            self,
            albums_by_id:dict[int,Album],
            artists_by_id:dict[int,Artist],
            genres_by_id:dict[int,Genre],
    ):
        with open(self.tracks_file_name,encoding='cp1252',newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                track=Track(int(row['track_id']),row['track_title'])

                artist_id = int(row['artist_id'])
                artist = artists_by_id.get(artist_id)
                if artist is None:
                    artist = Artist(artist_id,row['artist_name'])
                    artists_by_id[artist_id] = artist
                    self.dataset_of_artists.add(artist)
                track.artist=artist

                album_id = self.__optional_int(row['album_id'])
                if album_id is not None and album_id in albums_by_id:
                    track.album = albums_by_id[album_id]

                track.track_duration = self.__optional_duration(row['track_duration'])
                track.track_url = self.__optional_text(row['track_url'])
                # however,the format of genres is a little bit different
                # such as track_genres = "[{'genre_id': '21', 'genre_title': 'Hip-Hop'}, {'genre_id': '38', 'genre_title': 'Experimental'}]"
                if row['track_genres'].strip() == '':
                    genre_records = []
                else:
                    genre_records = ast.literal_eval(row['track_genres'])
                # The above method helps us convert the string into a python object

                for genre_record in genre_records:
                    genre_id = int(genre_record['genre_id'])
                    genre = genres_by_id.get(genre_id)
                    if genre is None:
                        genre = Genre(genre_id,genre_record['genre_title'])
                        genres_by_id[genre_id] = genre
                        self.dataset_of_genres.add(genre)

                    track.add_genre(genre)

                self.dataset_of_tracks.add(track)

    # Helper methods convert empty CSV cells into None for optional fields.
    @staticmethod
    def __optional_int(raw_value: str) -> int | None:
        """Convert a CSV integer field, treating an empty cell as missing data."""
        stripped_value = raw_value.strip()
        if stripped_value == '': return None
        else : return int(stripped_value)

    @staticmethod
    def __optional_duration(raw_value: str) -> int | None:
        """Convert whole or fractional CSV seconds to the Track model's integer seconds."""
        stripped_value = raw_value.strip()
        if stripped_value == '': return None

        # Most source values are integers, but a few contain a fractional number
        # of seconds (for example "61.56666667"). Track deliberately models
        # duration as whole seconds, so rounding belongs at this input boundary.
        else: return round(float(stripped_value))

    @staticmethod
    def __optional_text(raw_value: str) -> str | None:
        """Convert a CSV text field, treating whitespace-only cells as missing."""
        stripped_value = raw_value.strip()
        if stripped_value == '': return None
        else : return stripped_value