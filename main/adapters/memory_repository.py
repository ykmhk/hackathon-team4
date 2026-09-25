"""In-memory repository for the starter app."""

from main.adapters.repository import AbstractRepository
from main.domainmodel.user import User


class MemoryRepository(AbstractRepository):
    """Persist users in memory while the Flask app is running."""

    def __init__(self):
        self.__users: dict[str, User] = {}

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
