from werkzeug.security import generate_password_hash, check_password_hash

from medical_diary.domainmodel.user import User


class NameNotUniqueException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo):
    if repo.get_user(username) is not None:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash)
    repo.add_user(user)


def authenticate_user(username: str, password: str, repo) -> User:
    user = repo.get_user(username)
    if user is None or not check_password_hash(user.password_hash, password):
        raise AuthenticationException
    return user
