import abc
from typing import Optional, Iterable, TypeVar, Generic

from easyrepo.model.sorting import Sort

T = TypeVar("T")
ID = TypeVar("ID")


class CRUDRepository(Generic[T, ID], abc.ABC):
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
    def delete_all_by_id(self, ids: Iterable[ID]):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_by_id(self, id: ID):
        raise NotImplementedError()

    @abc.abstractmethod
    def exists_by_id(self, id: ID) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self, sort: Sort = None) -> Iterable[T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all_by_id(self, ids: Iterable[ID]) -> Iterable[T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, id: ID) -> Optional[T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, model: T) -> T:
        raise NotImplementedError()

    @abc.abstractmethod
    def save_all(self, models: Iterable[T]) -> Iterable[T]:
        raise NotImplementedError()
