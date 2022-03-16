import abc

from easyrepo.interface.crud import CRUDRepository, T, ID
from easyrepo.model.paging import PageRequest, Page
from easyrepo.model.sorting import Sort


class PagingRepository(CRUDRepository[T, ID]):
    """
    Extension of CrudRepository to provide additional method to retrieve entities using the pagination.
    """

    @abc.abstractmethod
    def find_page(self, page_request: PageRequest, sort: Sort = None) -> Page[T]:
        raise NotImplementedError()
