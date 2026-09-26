class Review:
    def __init__(self, review_id, user, track, rating, review_text, date):
        if type(review_id) is not int or review_id < 0:
            raise ValueError("Review ID should be a non-negative integer.")
        if type(rating) is not int or rating < 0 or rating > 5:
            raise ValueError("Rating should be a non-negative integer between 0 and 5.")
        if type(review_text) is not str or review_text.strip() == "":
            raise ValueError("Review text should be a non-empty string.")
        self.__review_id = review_id
        self.__user = user
        self.__track = track
        self.__rating = rating
        self.__review_text = review_text
        self.__date = date

    @property
    def review_id(self):
        return self.__review_id

    @property
    def user(self):
        return self.__user

    @property
    def track(self):
        return self.__track

    @property
    def rating(self):
        return self.__rating

    @property
    def review_text(self):
        return self.__review_text

    @property
    def date(self):
        return self.__date

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.review_id == other.review_id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return NotImplemented
        return self.review_id < other.review_id

    def __hash__(self):
        return hash(self.review_id)

    def __repr__(self):
        return f"<Review {self.review_id}, rating = {self.rating}>"
