from typing import Optional, Iterable, List, Tuple

import pymongo
from bson import ObjectId

from easyrepo.interface.paging import PagingRepository
from easyrepo.model.paging import Page, PageRequest
from easyrepo.model.sorting import Sort


class MongoRepository(PagingRepository[dict, ObjectId]):
    """
    Mongo repository.
    """

    def __init__(self, collection: pymongo.collection.Collection):
        self.collection = collection

    def count(self) -> int:
        """
        Returns the number of documents available.
        """
        return self.collection.estimated_document_count()

    def delete_all(self):
        """
        Deletes all documents.
        """
        self.collection.drop()

    def delete_all_by_id(self, ids: Iterable[ObjectId]):
        """
        Deletes all documents with the given IDs.
        """
        self.collection.delete_many({"_id": {"$in": ids}})

    def delete_by_id(self, id: ObjectId):
        """
        Deletes the document with the given id.
        """
        self.collection.delete_one({"_id": id})

    def exists_by_id(self, id: ObjectId) -> bool:
        """
        Returns whether a document with the given id exists.
        """
        return bool(self.collection.count_documents({"_id": id}))

    def find_all(self, sort: Sort = None) -> Iterable[dict]:
        """
        Returns all documents sorted by the given options.
        """
        args = {
            "filter": self._filter_query(),
            "sort": self._sort_query(sort)
        }
        return list(self.collection.find(**args))

    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[dict]:
        """
        Returns a Page of document meeting the paging restriction.
        """
        args = {
            "filter": self._filter_query(),
            "sort": self._sort_query(sort),
            "skip": page_request.offset(),
            "limit": page_request.size
        }
        result = list(self.collection.find(**args))
        return Page(content=result, page_request=page_request, total_elements=self.count())

    def find_all_by_id(self, ids: Iterable[ObjectId]) -> Iterable[dict]:
        """
        Returns all documents with the given IDs.
        """
        return list(self.collection.find(filter={"_id": {"$in": ids}}))

    def find_by_id(self, id: ObjectId) -> Optional[dict]:
        """
        Returns a document by its id.
        """
        return self.collection.find_one({"_id": id})

    def save(self, document: dict) -> dict:
        """
        Saves a given document.
        """
        if "_id" not in document:
            id = self.collection.insert_one(document).inserted_id
        else:
            id = document["_id"]
            self.collection.replace_one({"_id":id}, document)
        return self.find_by_id(id)

    def save_all(self, models: Iterable[dict]) -> Iterable[dict]:
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
