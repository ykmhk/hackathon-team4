from music.domainmodel.track import Track
# can't import user, would form circular import error as user imports favourite too.

class Favourite:

    def __init__(self, favourite_id: int, user, track: Track):
        if type(favourite_id) is not int or favourite_id < 0:
            raise ValueError('Favourite ID should be an integer')
        self.__favourite_id = favourite_id

        # correct instances
        from music.domainmodel.user import User
        if not isinstance(user, User):
            raise ValueError('User must be a valid User instance')
        self.__user = user

        if not isinstance(track, Track):
            raise ValueError('Track must be a valid Track instance!')
        self.__track = track


    @property
    def favourite_id(self) -> int:
        return self.__favourite_id

    @property
    def user(self):
        return self.__user

    @property
    def track(self) -> Track:
        return self.__track

    def __repr__(self) -> str:
        return f'<Favourite {self.favourite_id}, User: {self.user.user_name}, Track: {self.track.title}>'

    def __eq__(self, other: object) -> bool:
        # only when favourite_id is equal
        if not isinstance(other, self.__class__):
            return False
        return self.favourite_id == other.favourite_id

    def __lt__(self, other) -> bool:
        # compare by id
        if not isinstance(other, self.__class__):
            return True
        return self.favourite_id < other.favourite_id

    def __hash__(self) -> int:
        return hash(self.favourite_id)


# Reason for not adding a setter to the class:
# Favourite only represents the user-track association of 'someone favourites a song'.
# changing the user or track would represent a different favourite
# so relationship is managed by adding/removing Favourite objects from User (which user class defined already).
# attributes are read-only because no need for modify.

# But it still depends on how we are going to use this property.
    # @user.setter
    # def user(self, user: User):
    #     if not isinstance(user, User):
    #         raise ValueError('User must be a valid User instance!')
    #     self.__user = user
    #
    # @track.setter
    # def track(self, track: Track):
    #     if not isinstance(track, Track):
    #         raise ValueError('Track must be a valid Track instance!')
    #     self.__track = track