class User:

    def __init__(self, user_id: int, user_name: str, password: str):
        if type(user_id) is not int or user_id < 0:
            raise ValueError("User ID should be a non negative integer.")
        self.__user_id = user_id

        if type(user_name) is not str or user_name.strip() == '':
            raise ValueError("User name should be a non-empty string.")
        self.__user_name = user_name.lower().strip()

        if not isinstance(password, str) or len(password) < 7:
            raise ValueError("Password should be a string of at least 7 characters.")
        self.__password = password

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    def __repr__(self):
        return f'<User {self.user_name}, user id = {self.user_id}>'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.user_id < other.user_id

    def __hash__(self):
        return hash(self.user_id)
