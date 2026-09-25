"""In-memory implementation of the Music Library repository contract."""

from music.adapters.repository import AbstractRepository
from music.domainmodel.favourite import Favourite
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User


class MemoryRepository(AbstractRepository):
    """Store Music Library objects in memory while the Flask app is running."""



    def __init__(self):
        self.__tracks: dict[int, Track] = {}
        # Usernames are the lookup key because users log in with a username.
        self.__users: dict[str, User] = {}
        """dict[key,value]"""
        self.__favourites: list[Favourite] = []
        self.__reviews: list[Review] = []

    def add_track(self, track: Track) -> None:
        """Add a Track, or replace the stored Track with the same ID."""
        self.__tracks[track.track_id] = track

    def get_track(self, track_id: int) -> Track | None:
        """Return one Track by ID; ``dict.get`` naturally returns None if absent."""
        return self.__tracks.get(track_id)

    def get_all_tracks(self) -> list[Track]:
        """Return a list copy so callers cannot mutate the dictionary itself."""
        return list(self.__tracks.values())


    def add_favourite(self, favourite: Favourite) -> None:
        existing_favourite = self.get_favourite(
            favourite.user,
            favourite.track,
        )

        if existing_favourite is None:
            self.__favourites.append(favourite)

    def remove_favourite(self, favourite: Favourite) -> None:
        if favourite in self.__favourites:
            self.__favourites.remove(favourite)

    def get_favourites_for_user(self, user: User) -> list[Favourite]:
        return [
            favourite
            for favourite in self.__favourites
            if favourite.user == user
        ]

    def get_favourite(
            self,
            user: User,
            track: Track,
    ) -> Favourite | None:
        for favourite in self.__favourites:
            if favourite.user == user and favourite.track == track:
                return favourite

        return None

    def get_number_of_favourites(self) -> int:
        return len(self.__favourites)

    def add_review(self, review: Review) -> None:
        """Store one Review without imposing a one-review-per-user rule."""
        self.__reviews.append(review)

    def get_reviews_for_track(self, track: Track) -> list[Review]:
        """Return every stored Review that belongs to ``track``."""
        return [review for review in self.__reviews if review.track == track]

    def get_number_of_reviews(self) -> int:
        """Return how many Reviews are currently stored."""
        return len(self.__reviews)

    def add_user(self, user: User) -> None:
        """Store a User unless their normalized username is already taken."""
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance.")

        if self.get_user(user.user_name) is not None:
            raise ValueError("A user with this username already exists.")

        self.__users[user.user_name] = user

    def get_user(self, user_name: str) -> User | None:
        """Return a User by normalized username, or None if it is not stored."""
        if not isinstance(user_name, str):
            return None

        normalized_user_name = user_name.strip().lower()
        return self.__users.get(normalized_user_name)

    def get_number_of_users(self) -> int:
        """Return how many User objects are currently stored."""
        return len(self.__users)
      
    def search_tracks(self, query: str, criterion: str,) -> list[Track]:
        query = query.lower()
        results = []
        for track in self.__tracks.values():
            if criterion == "title":
                if query in track.title.lower():
                    results.append(track)
            elif criterion == "artist":
                if track.artist is not None and query in track.artist.full_name.lower():
                    results.append(track)
            elif criterion == "album":
                if track.album is not None and query in track.album.title.lower():
                    results.append(track)
            elif criterion == "genre":
                for genre in track.genres:
                    if query in genre.name.casefold():
                        results.append(track)
                        break

        return results
