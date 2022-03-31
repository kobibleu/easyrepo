import abc

from easyrepo.model.sorting import Sort


class CRUDRepository(abc.ABC):
    """
    Interface for generic CRUD operations for a specific type.
    """

    @abc.abstractmethod
    def count(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_all_by_id(self, ids):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_by_id(self, id):
        raise NotImplementedError()

    @abc.abstractmethod
    def exists_by_id(self, id):
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self, sort: Sort = None):
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all_by_id(self, ids):
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, model):
        raise NotImplementedError()

    @abc.abstractmethod
    def save_all(self, models):
        raise NotImplementedError()
