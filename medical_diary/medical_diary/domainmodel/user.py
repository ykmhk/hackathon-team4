class User:
    """A registered user of the Medical History Diary."""

    def __init__(self, username: str, password_hash: str,
                 full_name: str = "", date_of_birth: str = ""):
        self.__username = username
        self.__password_hash = password_hash
        self.full_name = full_name
        self.date_of_birth = date_of_birth

        # Healthcare provider information
        self.provider_name = ""
        self.provider_address = ""
        self.provider_email = ""
        self.provider_phone = ""
        self.provider_hours = ""

        # GP details
        self.gp_name = ""
        self.gp_practice = ""
        self.gp_email = ""
        self.gp_phone = ""

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.__username == other.username

    def __hash__(self):
        return hash(self.__username)
