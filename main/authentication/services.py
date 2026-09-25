"""Business rules for registering and authenticating app users."""

from werkzeug.security import check_password_hash, generate_password_hash

from main.adapters.repository import AbstractRepository
from main.domainmodel.user import User


def register_user(
    user_name: str,
    password: str,
    repository: AbstractRepository,
) -> User:
    """Create, securely store, and return a newly registered User.

    The repository checks username availability. The service owns password
    hashing and User ID allocation because these are authentication rules,
    rather than raw data-storage operations.
    """
    if repository.get_user(user_name) is not None:
        raise ValueError("This username is already taken.")

    next_user_id = repository.get_number_of_users() + 1
    password_hash = generate_password_hash(password)

    user = User(next_user_id, user_name, password_hash)
    repository.add_user(user)

    return user


def authenticate_user(
    user_name: str,
    password: str,
    repository: AbstractRepository,
) -> User | None:
    """Return the User for valid credentials, otherwise return None."""
    user = repository.get_user(user_name)

    if user is None or not isinstance(password, str):
        return None

    if check_password_hash(user.password, password):
        return user

    return None