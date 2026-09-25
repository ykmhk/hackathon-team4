class PlaceholderItem:
    """Simple neutral placeholder model for a starter project."""

    def __init__(self, item_id: int, title: str):
        if type(item_id) is not int or item_id < 0:
            raise ValueError("Item ID should be a non-negative integer.")
        self.__item_id = item_id

        if type(title) is not str or title.strip() == '':
            raise ValueError("Title should be a non-empty string.")
        self.__title = title.strip()

    @property
    def item_id(self) -> int:
        return self.__item_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        if type(new_title) is not str or new_title.strip() == '':
            raise ValueError("Title should be a non-empty string.")
        self.__title = new_title.strip()

    def __repr__(self):
        return f"<PlaceholderItem {self.title}, item id = {self.item_id}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.item_id == other.item_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.item_id < other.item_id

    def __hash__(self):
        return hash(self.item_id)
