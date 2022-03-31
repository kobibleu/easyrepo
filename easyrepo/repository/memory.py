from typing import Iterable, Optional, TypeVar, Generic, get_args

from pydantic import BaseModel

from easyrepo import PagingRepository
from easyrepo.model.paging import PageRequest, Page
from easyrepo.model.sorting import Sort

T = TypeVar("T")


class MemoryRepository(Generic[T], PagingRepository):
    """
    Memory repository.
    """

    def __init__(self):
        self._data = {}
        model_type = get_args(self.__orig_bases__[0])[0]
        if not issubclass(model_type, (BaseModel, dict)):
            raise ValueError(f"Model type {model_type} is not a pydantic model or dict")

    def count(self) -> int:
        """
        Returns the number of entities available.
        """
        return len(self._data)

    def delete_all(self):
        """
        Deletes all entities.
        """
        self._data.clear()

    def delete_all_by_id(self, ids: Iterable[int]):
        """
        Deletes all entities with the given IDs.
        """
        for id in ids:
            self._data.pop(id)

    def delete_by_id(self, id: int):
        """
        Deletes the entity with the given id.
        """
        self._data.pop(id)

    def exists_by_id(self, id: int) -> bool:
        """
        Returns whether a document with the given id exists.
        """
        return self._data.get(id, None) is not None

    def find_all(self, sort: Sort = None) -> Iterable[T]:
        """
        Returns all entities sorted by the given options.
        """
        return list(self._data.values())

    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[T]:
        """
        Returns a Page of entities meeting the paging restriction.
        """
        result = self.find_all(sort)[page_request.offset():page_request.offset() + page_request.size]
        return Page(content=result, page_request=page_request, total_elements=self.count())

    def find_all_by_id(self, ids: Iterable[int]) -> Iterable[T]:
        """
        Returns all entities with the given IDs.
        """
        return {k: self._data[k] for k in ids}

    def find_by_id(self, id: int) -> Optional[T]:
        """
        Returns an entity by its id.
        """
        return self._data.get(id)

    def save(self, model: T) -> T:
        """
        Saves a given entity.
        """
        next_id = len(self._data) + 1
        if isinstance(model, dict):
            return self._save_dict_model(model, next_id)
        elif isinstance(model, BaseModel):
            return self._save_pydantic_model(model, next_id)
        else:
            raise ValueError(f"type {type(model)} not handled by repository.")

    def save_all(self, models: Iterable[T]) -> Iterable[T]:
        """
        Saves all given entities.
        """
        return [self.save(entity) for entity in models]

    def _save_dict_model(self, model: dict, next_id: int):
        """
        Save a dict type model.
        """
        if "id" in model:
            self._data[model["id"]] = model
            return model
        model["id"] = next_id
        self._data[next_id] = model
        return model

    def _save_pydantic_model(self, model: BaseModel, next_id: int):
        """
        Save a pydantic.BaseModel subclass type model.
        """
        if hasattr(model, "id") and model.id is not None:
            self._data[model.id] = model
            return model
        model.id = next_id
        self._data[next_id] = model
        return model
