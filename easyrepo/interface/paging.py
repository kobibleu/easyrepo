import abc
from typing import Any

from easyrepo.interface.crud import CRUDRepository
from easyrepo.model.paging import PageRequest, Page
from easyrepo.model.sorting import Sort


class PagingRepository(CRUDRepository):
    """
    Extension of CrudRepository to provide additional method to retrieve entities using the pagination.
    """

    @abc.abstractmethod
    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[Any]:
        raise NotImplementedError()
