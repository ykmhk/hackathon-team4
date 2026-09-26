class Album:

    def __init__(self, album_id: int, album_title: str):
        if type(album_id) is not int or album_id < 0:
            raise ValueError("Album ID should be a non negative integer.")
        self.__album_id = album_id

        if type(album_title) is not str or album_title.strip() == '':
            raise ValueError("Album title should be a non-empty string.")
        self.__title = album_title.strip()

        self.__release_year: int | None = None
        self.__total_tracks: int | None = None
        self.__album_url: str | None = None
        self.__album_type: str | None = None
        # self.__album_image: str | None = None

    @property
    def album_id(self) -> int:
        return self.__album_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        if type(new_title) is not str or new_title.strip() == '':
            raise ValueError("Album title should be a non-empty string.")
        self.__title = new_title.strip()

    @property
    def release_year(self) -> int | None:
        return self.__release_year

    @release_year.setter
    def release_year(self, new_release_year: int | None):
        if new_release_year is None:
            self.__release_year = None
        elif type(new_release_year) is int and new_release_year >= 0:
            self.__release_year = new_release_year
        else:
            raise ValueError("release_year must be a non-negative int or None.")

    @property
    def total_tracks(self) -> int | None:
        return self.__total_tracks

    @total_tracks.setter
    def total_tracks(self, new_total_tracks: int | None):
        if new_total_tracks is None:
            self.__total_tracks = None
        elif type(new_total_tracks) is int and new_total_tracks >= 0:
            self.__total_tracks = new_total_tracks
        else:
            raise ValueError("total_tracks must be a non-negative int or None.")

    @property
    def album_url(self) -> str | None:
        return self.__album_url

    @album_url.setter
    def album_url(self, new_album_url: str | None):
        if new_album_url is None:
            self.__album_url = None
        elif type(new_album_url) is str and new_album_url.strip() != '':
            self.__album_url = new_album_url.strip()
        else:
            raise ValueError("album_url must be a non-empty string or None.")

    @property
    def album_type(self) -> str | None:
        return self.__album_type

    @album_type.setter
    def album_type(self, new_album_type: str | None):
        if new_album_type is None:
            self.__album_type = None
        elif type(new_album_type) is str and new_album_type.strip() != '':
            self.__album_type = new_album_type.strip()
        else:
            raise ValueError("album_type must be a non-empty string or None.")
    #
    # @property
    # def album_image(self) -> str | None:
    #     return self.__album_image
    #
    # @album_image.setter
    # def album_image(self, new_album_image: str | None):
    #     if new_album_image is None:
    #         self.__album_image = None
    #     elif type(new_album_image) is str and new_album_image.strip() != '':
    #         self.__album_image = new_album_image.strip()
    #     else:
    #         raise ValueError("album_image must be a non-empty string or None.")


    def __repr__(self):
        return f"<Album {self.title}, album id = {self.album_id}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.album_id == other.album_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.album_id < other.album_id

    def __hash__(self):
        return hash(self.album_id)
