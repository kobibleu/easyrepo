from typing import Optional, Iterable, List, Tuple, TypeVar, Generic, get_args

import pymongo
from bson import ObjectId
from pydantic import BaseModel

from easyrepo.interface.paging import PagingRepository
from easyrepo.model.paging import Page, PageRequest
from easyrepo.model.sorting import Sort

T = TypeVar("T")


class MongoRepository(Generic[T], PagingRepository):
    """
    Mongo repository.
    """

    def __init__(self, collection: pymongo.collection.Collection):
        self._collection = collection
        self._model_type = get_args(self.__orig_bases__[0])[0]
        if not issubclass(self._model_type, (BaseModel, dict)):
            raise ValueError(f"Model type {self._model_type} is not a pydantic model or dict")
        self._is_pydantic_model = issubclass(self._model_type, BaseModel)

    def count(self) -> int:
        """
        Returns the number of documents available.
        """
        return self._collection.estimated_document_count()

    def delete_all(self):
        """
        Deletes all documents.
        """
        self._collection.drop()

    def delete_all_by_id(self, ids: Iterable[ObjectId]):
        """
        Deletes all documents with the given IDs.
        """
        self._collection.delete_many({"_id": {"$in": ids}})

    def delete_by_id(self, id: ObjectId):
        """
        Deletes the document with the given id.
        """
        self._collection.delete_one({"_id": id})

    def exists_by_id(self, id: ObjectId) -> bool:
        """
        Returns whether a document with the given id exists.
        """
        return bool(self._collection.count_documents({"_id": id}))

    def find_all(self, sort: Sort = None) -> Iterable[T]:
        """
        Returns all documents sorted by the given options.
        """
        args = {
            "filter": self._filter_query(),
            "sort": self._sort_query(sort)
        }
        result = list(self._collection.find(**args))
        if self._is_pydantic_model:
            result = [self._model_type(id=r.pop("_id"), **r) for r in result]
        return result

    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[T]:
        """
        Returns a Page of document meeting the paging restriction.
        """
        args = {
            "filter": self._filter_query(),
            "sort": self._sort_query(sort),
            "skip": page_request.offset(),
            "limit": page_request.size
        }
        result = list(self._collection.find(**args))
        if self._is_pydantic_model:
            result = [self._model_type(id=r.pop("_id"), **r) for r in result]
        return Page(content=result, page_request=page_request, total_elements=self.count())

    def find_all_by_id(self, ids: Iterable[ObjectId]) -> Iterable[T]:
        """
        Returns all documents with the given IDs.
        """
        result = list(self._collection.find(filter={"_id": {"$in": ids}}))
        if self._is_pydantic_model:
            result = [self._model_type(id=r.pop("_id"), **r) for r in result]
        return result

    def find_by_id(self, id: ObjectId) -> Optional[T]:
        """
        Returns a document by its id.
        """
        result = self._collection.find_one({"_id": id})
        if self._is_pydantic_model:
            result = self._model_type(id=result.pop("_id"), **result)
        return result

    def save(self, model: T) -> T:
        """
        Saves a given document.
        """
        if isinstance(model, BaseModel):
            model = model.dict()
            model["_id"] = model.pop("id", None)
        elif not isinstance(model, dict):
            raise ValueError(f"type {type(model)} not handled by repository.")

        if model.get("_id") is None:
            model.pop("_id", None)
            id = self._collection.insert_one(model).inserted_id
        else:
            id = model["_id"]
            self._collection.replace_one({"_id": id}, model)
        return self.find_by_id(id)

    def save_all(self, models: Iterable[T]) -> Iterable[T]:
        """
        Saves all given documents.
        """
        return [self.save(model) for model in models]

    @staticmethod
    def _filter_query(filter: dict = None) -> dict:
        if filter is None:
            return {}
        return {}

    @staticmethod
    def _sort_query(sort: Sort) -> List[Tuple[str, int]]:
        if sort is None:
            return []
        query = []
        for order in sort.orders:
            direction = pymongo.ASCENDING if order.direction.is_ascending() else pymongo.DESCENDING
            query.append((order.key, direction))
        return query
