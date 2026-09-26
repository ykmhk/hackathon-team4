from music.adapters.repository import AbstractRepository
from music.domainmodel.favourite import Favourite
from music.domainmodel.user import User


def add_favourite(
        user: User,
        track_id: int,
        repository: AbstractRepository,
) -> Favourite:
    track = repository.get_track(track_id)

    if track is None:
        raise ValueError(f"Track with ID {track_id} does not exist.")

    existing_favourite = repository.get_favourite(user, track)

    if existing_favourite is not None:
        return existing_favourite

    favourite = Favourite(
        repository.get_number_of_favourites() + 1,
        user,
        track,
    )

    repository.add_favourite(favourite)
    user.add_favourite(favourite)

    return favourite


def remove_favourite(
        user: User,
        track_id: int,
        repository: AbstractRepository,
) -> None:
    track = repository.get_track(track_id)

    if track is None:
        raise ValueError(f"Track with ID {track_id} does not exist.")

    favourite = repository.get_favourite(user, track)

    if favourite is None:
        return

    repository.remove_favourite(favourite)
    user.remove_favourite(favourite)


def get_favourites_for_user(
        user: User,
        repository: AbstractRepository,
) -> list[Favourite]:
    return repository.get_favourites_for_user(user)

def is_favourite(username: str,track_id: int,repository: AbstractRepository,) -> bool:
    user = repository.get_user(username)
    track = repository.get_track(track_id)

    if user is None or track is None:
        return False

    return repository.get_favourite(user, track) is not None