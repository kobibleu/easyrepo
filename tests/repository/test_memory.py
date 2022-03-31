from typing import Optional

import pytest
from pydantic import BaseModel

from easyrepo.model.paging import PageRequest
from easyrepo.repository.memory import MemoryRepository


class TestModel(BaseModel):
    id: Optional[int]
    name: str


class DictRepo(MemoryRepository[dict]):
    pass


class ModelRepo(MemoryRepository[TestModel]):
    pass


class IntRepo(MemoryRepository[int]):
    pass


@pytest.fixture
def dict_repo():
    repo = DictRepo()
    repo._data = {
        1: {"id": 1, "name": "entity1"},
        2: {"id": 2, "name": "entity2"},
        3: {"id": 3, "name": "entity3"}
    }
    yield repo


@pytest.fixture
def model_repo():
    repo = ModelRepo()
    yield repo


def test_create_repo_with_unexpected_model_type():
    with pytest.raises(ValueError):
        IntRepo()


def test_count(dict_repo):
    assert dict_repo.count() == 3


def test_delete_all(dict_repo):
    dict_repo.delete_all()
    assert dict_repo.count() == 0


def test_delete_all_by_id(dict_repo):
    dict_repo.delete_all_by_id([1, 2])
    assert dict_repo.count() == 1


def test_delete_by_id(dict_repo):
    dict_repo.delete_by_id(1)
    assert dict_repo.count() == 2


def test_exists_by_id(dict_repo):
    assert dict_repo.exists_by_id(1)
    assert not dict_repo.exists_by_id(4)


def test_find_all(dict_repo):
    assert len(dict_repo.find_all()) == 3


def test_find_page(dict_repo):
    res = dict_repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_all_by_id(dict_repo):
    assert len(dict_repo.find_all_by_id([1, 2])) == 2


def test_find_by_id(dict_repo):
    assert dict_repo.find_by_id(1)["name"] == "entity1"
    assert dict_repo.find_by_id(4) is None


def test_save_dict_type(dict_repo):
    res = dict_repo.save({"name": "entity4"})
    assert res["id"] == 4
    res["name"] = "entity4bis"
    res = dict_repo.save(res)
    assert res["name"] == "entity4bis"


def test_save_pydantic_model_type(model_repo):
    res = model_repo.save(TestModel(name="entity1"))
    assert res.id == 1
    res.name = "entity1bis"
    res = model_repo.save(res)
    assert res.name == "entity1bis"


def test_save_unexpected_type(dict_repo):
    with pytest.raises(ValueError):
        dict_repo.save(1)


def test_save_dict_type_list(dict_repo):
    res = dict_repo.save_all([{"id": 3, "name": "entity3bis"}, {"name": "entity4"}, {"name": "entity5"}])
    assert len(res) == 3
    assert len(dict_repo.find_all()) == 5
    assert dict_repo.find_by_id(3)["name"] == "entity3bis"


def test_save_pydantic_model_type_list(model_repo):
    res = model_repo.save_all([TestModel(name="entity1"), TestModel(name="entity2"), TestModel(name="entity3")])
    assert len(res) == 3
