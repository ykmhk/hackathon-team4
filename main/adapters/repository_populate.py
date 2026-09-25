"""Repository seeding hook for the starter app."""

from pathlib import Path

from main.adapters.repository import AbstractRepository


def populate_repository(
    repository: AbstractRepository,
    albums_file_path: str | Path | None = None,
    tracks_file_path: str | Path | None = None,
) -> None:
    """No-op seeder for a generic starter app.

    Replace this with any real initialization logic needed by your project.
    """
    return None
