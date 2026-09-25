"""Abstract repository contract for a simple starter app."""

from abc import ABC, abstractmethod

from main.domainmodel.user import User


class AbstractRepository(ABC):
    """Define the generic storage contract used by the starter app."""

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
        """Return the number of stored Users."""
        raise NotImplementedError
