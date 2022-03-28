import pytest

from easyrepo import MemoryRepository
from easyrepo.model.paging import PageRequest


@pytest.fixture
def repo():
    repo = MemoryRepository()
    repo._data = {
        1: {"id": 1, "name": "entity1"},
        2: {"id": 2, "name": "entity2"},
        3: {"id": 3, "name": "entity3"}
    }
    yield repo


def test_count(repo):
    assert repo.count() == 3


def test_delete_all(repo):
    repo.delete_all()
    assert repo.count() == 0


def test_delete_all_by_id(repo):
    repo.delete_all_by_id([1, 2])
    assert repo.count() == 1


def test_delete_by_id(repo):
    repo.delete_by_id(1)
    assert repo.count() == 2


def test_exists_by_id(repo):
    assert repo.exists_by_id(1)
    assert not repo.exists_by_id(4)


def test_find_all(repo):
    assert len(repo.find_all()) == 3


def test_find_page(repo):
    res = repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_all_by_id(repo):
    assert len(repo.find_all_by_id([1, 2])) == 2


def test_find_by_id(repo):
    assert repo.find_by_id(1)["name"] == "entity1"
    assert repo.find_by_id(4) is None


def test_save(repo):
    res = repo.save({"name": "entity4"})
    assert res["id"] == 4
    res["name"] = "entity4bis"
    res = repo.save(res)
    assert res["name"] == "entity4bis"


def test_save_all(repo):
    res = repo.save_all([{"id": 3, "name": "entity3bis"}, {"name": "entity4"}, {"name": "entity5"}])
    assert len(res) == 3
    assert len(repo.find_all()) == 5
    assert repo.find_by_id(3)["name"] == "entity3bis"
