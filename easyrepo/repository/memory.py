from typing import Iterable, Optional

from easyrepo import PagingRepository
from easyrepo.model.paging import PageRequest, Page
from easyrepo.model.sorting import Sort


class MemoryRepository(PagingRepository[dict, int]):
    """
    Memory repository.
    """

    def __init__(self):
        self._data = {}

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

    def find_all(self, sort: Sort = None) -> Iterable[dict]:
        """
        Returns all entities sorted by the given options.
        """
        return list(self._data.values())

    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[dict]:
        """
        Returns a Page of entities meeting the paging restriction.
        """
        result = self.find_all(sort)[page_request.offset():page_request.offset() + page_request.size]
        return Page(content=result, page_request=page_request, total_elements=self.count())

    def find_all_by_id(self, ids: Iterable[int]) -> Iterable[dict]:
        """
        Returns all documents with the given IDs.
        """
        return {k: self._data[k] for k in ids}

    def find_by_id(self, id: int) -> Optional[dict]:
        """
        Returns a document by its id.
        """
        return self._data.get(id)

    def save(self, entity: dict) -> dict:
        """
        Saves a given document.
        """
        if "id" in entity:
            self._data[entity["id"]] = entity
            return entity

        next_id = len(self._data) + 1
        entity["id"] = next_id
        self._data[next_id] = entity
        return entity

    def save_all(self, models: Iterable[dict]) -> Iterable[dict]:
        """
        Saves all given documents.
        """
        return [self.save(model) for model in models]
