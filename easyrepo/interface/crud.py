import abc
from typing import List, Any

from easyrepo.model.sorting import Sort


class CRUDRepository(abc.ABC):
    """
    Interface for generic CRUD operations for a specific type.
    """

    @abc.abstractmethod
    def count(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_all_by_id(self, ids: List[Any]):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_by_id(self, id: Any):
        raise NotImplementedError()

    @abc.abstractmethod
    def exists_by_id(self, id: Any) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self, sort: Sort = None) -> List[Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all_by_id(self, ids: List[Any]) -> List[Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, id: Any) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, model: Any) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def save_all(self, models: List[Any]) -> List[Any]:
        raise NotImplementedError()
