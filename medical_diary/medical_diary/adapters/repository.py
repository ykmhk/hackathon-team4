import abc

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def add_record(self, record):
        raise NotImplementedError

    @abc.abstractmethod
    def get_records_for_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def get_record(self, record_id):
        raise NotImplementedError
