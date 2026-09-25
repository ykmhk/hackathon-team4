"""Abstract data-access contract for the Music Library.

Services will depend on this contract rather than knowing whether Tracks are
stored in memory, in CSV files, or eventually in a database.
"""
from music.domainmodel.user import User
from abc import ABC, abstractmethod
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.track import Track


class AbstractRepository(ABC):
    """Define the data-access operations required by the Music Library."""

    @abstractmethod
    def add_track(self, track: Track) -> None:
        """Store a Track so that later application code can retrieve it."""
        raise NotImplementedError

    @abstractmethod
    def get_track(self, track_id: int) -> Track | None:
        """Return the Track with ``track_id``, or None when it is not stored."""
        raise NotImplementedError

    @abstractmethod
    def get_all_tracks(self) -> list[Track]:
        """Return all stored Tracks as a list for a service to process."""
        raise NotImplementedError

    @abstractmethod
    def add_favourite(self, favourite: Favourite) -> None:
        """Store a Favourite unless the relationship already exists."""
        raise NotImplementedError

    @abstractmethod
    def remove_favourite(self, favourite: Favourite) -> None:
        """Remove a stored Favourite."""
        raise NotImplementedError

    @abstractmethod
    def get_favourites_for_user(self, user: User) -> list[Favourite]:
        """Return all Favourites belonging to the given user."""
        raise NotImplementedError

    @abstractmethod
    def get_favourite(
            self,
            user: User,
            track: Track,
    ) -> Favourite | None:
        """Return the Favourite for a user-track pair, if it exists."""
        raise NotImplementedError

    @abstractmethod
    def get_number_of_favourites(self) -> int:
        """Return the number of stored Favourites."""
        raise NotImplementedError

    @abstractmethod
    def add_review(self, review: Review) -> None:
        """Store one Review."""
        raise NotImplementedError

    @abstractmethod
    def get_reviews_for_track(self, track: Track) -> list[Review]:
        """Return Reviews that belong to the given Track."""
        raise NotImplementedError

    @abstractmethod
    def get_number_of_reviews(self) -> int:
        """Return the number of stored Reviews."""
        raise NotImplementedError


    @abstractmethod
    def search_tracks(self, query: str, criterion: str,) -> list[Track]:
        """Return tracks matching the search query."""
        raise NotImplementedError




    @abstractmethod
    def add_user(self, user: User) -> None:
        """Store one User under their normalized username."""
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_name: str) -> User | None:
        """Return a User by username, or None when no such User is stored."""
        raise NotImplementedError

    @abstractmethod
    def get_number_of_users(self) -> int:
        """Return the number of stored Users for User ID allocation."""
        raise NotImplementedError
