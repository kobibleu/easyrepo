from typing import Optional, Iterable, List, Tuple, TypeVar, Generic, get_args

import pymongo
from bson import ObjectId
from easyrepo.model.mongo import MongoModel

from easyrepo.interface.paging import PagingRepository
from easyrepo.model.paging import Page, PageRequest
from easyrepo.model.sorting import Sort

T = TypeVar("T")


class MongoRepository(Generic[T], PagingRepository):
    """
    Mongo repository.

    T: the type of object handled by the repository, can be a dict or `easyrepo.model.mongo.MongoModel`.
    """

    def __init__(self, collection: pymongo.collection.Collection):
        self._collection = collection
        self._model_type = get_args(self.__orig_bases__[0])[0]
        if not issubclass(self._model_type, (MongoModel, dict)):
            raise ValueError(f"Model type {self._model_type} is not dict or `easyrepo.model.mongo.MongoModel`")
        self._is_pydantic_model = issubclass(self._model_type, MongoModel)

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
        return [self._map_result(r) for r in result]

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
        return Page(
            content=[self._map_result(r) for r in result],
            page_request=page_request,
            total_elements=self.count()
        )

    def find_all_by_id(self, ids: Iterable[ObjectId]) -> Iterable[T]:
        """
        Returns all documents with the given IDs.
        """
        result = list(self._collection.find(filter={"_id": {"$in": ids}}))
        return [self._map_result(r) for r in result]

    def find_by_id(self, id: ObjectId) -> Optional[T]:
        """
        Returns a document by its id.
        """
        result = self._collection.find_one({"_id": id})
        return self._map_result(result)

    def save(self, model: T) -> T:
        """
        Saves a given document.
        """
        if isinstance(model, MongoModel):
            model = model.dict()
            model["_id"] = model.pop("id", None)
        elif not isinstance(model, dict):
            raise ValueError(f"type {type(model)} not handled by repository.")

        model_id = model.get("_id")
        if model_id is None:
            model.pop("_id", None)  # ensure there is no `_id` field in the document to not create it with None value
            model_id = self._collection.insert_one(model).inserted_id
        else:
            self._collection.replace_one({"_id": model_id}, model)
        return self.find_by_id(model_id)

    def save_all(self, models: Iterable[T]) -> Iterable[T]:
        """
        Saves all given documents.
        """
        return [self.save(m) for m in models]

    @staticmethod
    def _filter_query(filter: dict = None) -> dict:
        """
        Build mongo filter query.
        """
        if filter is None:
            return {}
        return {}

    @staticmethod
    def _sort_query(sort: Sort) -> List[Tuple[str, int]]:
        """
        Build mongo sort query.
        """
        if sort is None:
            return []
        query = []
        for order in sort.orders:
            direction = pymongo.ASCENDING if order.direction.is_ascending() else pymongo.DESCENDING
            query.append((order.key, direction))
        return query

    def _map_result(self, result: dict) -> T:
        """
        Map query result into appropriate object.
        """
        if not self._is_pydantic_model:
            return result
        return self._model_type(id=result.pop("_id"), **result)
