from typing import TypeVar, Generic, get_args, Iterable, List, Optional

from sqlalchemy.orm import Session

from easyrepo import PagingRepository
from easyrepo.model.paging import PageRequest, Page
from easyrepo.model.sorting import Sort
from easyrepo.model.sql import Entity

T = TypeVar("T", bound=Entity)


class SqlRepository(Generic[T], PagingRepository):
    """
    SQL repository.

    T: the type of object handled by the repository, must be `easyrepo.model.sql.Entity`.
    """

    def __init__(self, session: Session):
        self._session = session
        self._model = get_args(self.__orig_bases__[0])[0]
        if type(self._model) == TypeVar:
            raise ValueError("Missing repository type")
        if not issubclass(self._model, Entity):
            raise ValueError(f"Model type {self._model} is not `easyrepo.model.sql.Entity`")

    def count(self) -> int:
        """
        Returns the number of entities available.
        """
        return self._session.query(self._model).count()

    def delete_all(self):
        """
        Deletes all entities.
        """
        self._session.query(self._model).delete()

    def delete_all_by_id(self, ids: Iterable[id]):
        """
        Deletes all entities with the given IDs.
        """
        self._session.query(self._model).filter(self._model.id.in_(ids)).delete()

    def delete_by_id(self, id: int):
        """
        Deletes the entity with the given id.
        """
        self._session.query(self._model).filter(self._model.id == id).delete()

    def exists_by_id(self, id: int) -> bool:
        """
        Returns whether an entity with the given id exists.
        """
        return bool(self._session.query(self._model).filter(self._model.id == id).count())

    def find_all(self, sort: Sort = None) -> List[T]:
        """
        Returns all entities sorted by the given options.
        """
        query = self._session.query(self._model)
        order_by = self._sort_query(sort)
        if order_by:
            query = query.order_by(*order_by)
        return query.all()

    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[T]:
        """
        Returns a Page of entities meeting the paging restriction.
        """
        query = self._session.query(self._model).offset(page_request.offset()).limit(page_request.size)
        order_by = self._sort_query(sort)
        if order_by:
            query = query.order_by(*order_by)
        result = query.all()
        return Page(
            content=result,
            page_request=page_request,
            total_elements=self.count()
        )

    def find_all_by_id(self, ids: Iterable[id]) -> List[T]:
        """
        Returns all entities with the given IDs.
        """
        return self._session.query(self._model).filter(self._model.id.in_(ids)).all()

    def find_by_id(self, id: id) -> Optional[T]:
        """
        Returns an entity by its id.
        """
        return self._session.query(self._model).filter(self._model.id == id).one_or_none()

    def save(self, model: T) -> T:
        """
        Saves a given entity.
        """
        if not isinstance(model, Entity):
            raise ValueError(f"type {type(model)} not handled by repository.")
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return model

    def save_all(self, models: Iterable[T]) -> List[T]:
        """
        Saves all given entities.
        """
        if any(not isinstance(m, Entity) for m in models):
            raise ValueError(f"one of type in the list of model is not handled by repository.")
        self._session.add_all(models)
        self._session.commit()
        for m in models:
            self._session.refresh(m)
        return list(models)

    def _sort_query(self, sort: Sort) -> List[str]:
        """
        Build sqlalchemy sort query.
        """
        if sort is None:
            return []
        query = []
        for order in sort.orders:
            attr = getattr(self._model, order.key)
            order_by = attr.asc() if order.direction.is_ascending() else attr.desc()
            query.append(order_by)
        return query
