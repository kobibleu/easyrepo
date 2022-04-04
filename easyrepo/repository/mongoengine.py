from typing import Optional, Iterable, List, TypeVar, Generic, get_args

from bson import ObjectId
from mongoengine import Document, DoesNotExist

from easyrepo.interface.paging import PagingRepository
from easyrepo.model.paging import Page, PageRequest
from easyrepo.model.sorting import Sort

T = TypeVar("T", bound=Document)


class MongoEngineRepository(Generic[T], PagingRepository):
    """
    Mongo repository dedicated to MongoEngine ODM.

    T: the type of object handled by the repository, must be `mongoengine.Document`.
    """

    def __init__(self):
        self._model_type = get_args(self.__orig_bases__[0])[0]
        if not issubclass(self._model_type, Document):
            raise ValueError(f"Model type {self._model_type} is not `mongoengine.Document`")

    def count(self) -> int:
        """
        Returns the number of documents available.
        """
        return self._model_type.objects.count()

    def delete_all(self):
        """
        Deletes all documents.
        """
        self._model_type.drop_collection()

    def delete_all_by_id(self, ids: Iterable[ObjectId]):
        """
        Deletes all documents with the given IDs.
        """
        self._model_type.objects(id__in=ids).delete()

    def delete_by_id(self, id: ObjectId):
        """
        Deletes the document with the given id.
        """
        self._model_type.objects(id=id).delete()

    def exists_by_id(self, id: ObjectId) -> bool:
        """
        Returns whether a document with the given id exists.
        """
        return bool(self._model_type.objects(id=id).count())

    def find_all(self, sort: Sort = None) -> List[T]:
        """
        Returns all documents sorted by the given options.
        """
        order_by = self._sort_query(sort)
        query_set = self._model_type.objects().order_by(*order_by)
        return list(query_set)

    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[T]:
        """
        Returns a Page of document meeting the paging restriction.
        """
        order_by = self._sort_query(sort)
        query_set = self._model_type.objects().skip(page_request.offset()).limit(page_request.size).order_by(*order_by)
        result = list(query_set)
        return Page(
            content=result,
            page_request=page_request,
            total_elements=self.count()
        )

    def find_all_by_id(self, ids: Iterable[ObjectId]) -> List[T]:
        """
        Returns all documents with the given IDs.
        """
        return list(self._model_type.objects(id__in=ids))

    def find_by_id(self, id: ObjectId) -> Optional[T]:
        """
        Returns a document by its id.
        """
        try:
            return self._model_type.objects(id=id).get()
        except DoesNotExist:
            return None

    def save(self, model: T) -> T:
        """
        Saves a given document.
        """
        if not isinstance(model, Document):
            raise ValueError(f"type {type(model)} not handled by repository.")
        model.save()
        model.reload()
        return model

    def save_all(self, models: Iterable[T]) -> List[T]:
        """
        Saves all given documents.
        """
        return [self.save(m) for m in models]

    @staticmethod
    def _sort_query(sort: Sort) -> List[str]:
        """
        Build mongoengine sort query.
        """
        if sort is None:
            return []
        query = []
        for order in sort.orders:
            direction = "+" if order.direction.is_ascending() else "-"
            query.append(f"{direction}{order.key}")
        return query
