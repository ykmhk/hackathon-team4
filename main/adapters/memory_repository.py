"""In-memory repository for the symptom checker."""


from main.adapters.repository import AbstractRepository


class MemoryRepository(AbstractRepository):
    """Store application data in memory."""

    def __init__(self):
        pass