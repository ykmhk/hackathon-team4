"""Unit tests for authentication business rules."""

import pytest
from werkzeug.security import check_password_hash

from music.adapters.memory_repository import MemoryRepository
from music.authentication import services


def test_register_user_hashes_password_and_stores_user():
    """Registration stores a new User with a hash rather than the raw password."""
    repository = MemoryRepository()

    user = services.register_user("Meti", "SecurePass1", repository)

    assert user.user_id == 1
    assert user.user_name == "meti"
    assert repository.get_user("meti") is user

    # A database/repository must never store this submitted password directly.
    assert user.password != "SecurePass1"
    assert check_password_hash(user.password, "SecurePass1")


def test_register_user_rejects_an_existing_username():
    """Registration rejects usernames that are already associated with an account."""
    repository = MemoryRepository()
    services.register_user("Meti", "SecurePass1", repository)

    with pytest.raises(ValueError, match="already taken"):
        services.register_user("METI", "AnotherPass1", repository)


def test_authenticate_user_returns_user_for_correct_credentials():
    """Correct username and password authenticate the stored User."""
    repository = MemoryRepository()
    registered_user = services.register_user("Meti", "SecurePass1", repository)

    authenticated_user = services.authenticate_user(
        "meti",
        "SecurePass1",
        repository,
    )

    assert authenticated_user is registered_user


def test_authenticate_user_returns_none_for_invalid_credentials():
    """An unknown username or wrong password must not authenticate a User."""
    repository = MemoryRepository()
    services.register_user("Meti", "SecurePass1", repository)

    assert services.authenticate_user("unknown", "SecurePass1", repository) is None
    assert services.authenticate_user("meti", "WrongPass1", repository) is None