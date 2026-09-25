"""Load the supplied CSV dataset into a repository when the app starts."""

from pathlib import Path

from music.adapters.csvdatareader import CSVDataReader
from music.adapters.repository import AbstractRepository


def populate_repository(
        repository: AbstractRepository,
        albums_file_path: str | Path | None = None,
        tracks_file_path: str | Path | None = None,
) -> None:
    """Load CSV Tracks from the supplied files into ``repository``.

    Lab 4 populates its repository from a four-item tuple list so students can
    focus on the pattern.  Assignment 1 already has a CSVDataReader, so this
    adapter reuses that completed input boundary and receives fully connected
    Track, Artist, Album, and Genre objects. When neither file is supplied,
    the application uses its full dataset. Tests can explicitly supply both
    small, controlled CSV fixture files instead.

    Supplying only one file would silently mix datasets, so it is rejected.
    """
    if (albums_file_path is None) != (tracks_file_path is None):
        raise ValueError(
            'Provide both albums_file_path and tracks_file_path, or neither.'
        )

    if albums_file_path is None:
        data_directory = Path(__file__).resolve().parent / 'data'
        albums_file_path = data_directory / 'raw_albums_excerpt.csv'
        tracks_file_path = data_directory / 'raw_tracks_excerpt.csv'

    csv_reader = CSVDataReader(
        str(albums_file_path),
        str(tracks_file_path),
    )
    csv_reader.read_csv_files()

    for track in csv_reader.dataset_of_tracks:
        repository.add_track(track)
