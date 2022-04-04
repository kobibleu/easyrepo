import pytest
from mongomock import MongoClient

from easyrepo.model.mongo import MongoModel
from easyrepo.model.paging import PageRequest
from easyrepo.repository.mongo import MongoRepository


class TestModel(MongoModel):
    value: str


class DictRepo(MongoRepository[dict]):
    pass


class ModelRepo(MongoRepository[TestModel]):
    pass


class IntRepo(MongoRepository[int]):
    pass


@pytest.fixture
def collection():
    collection = MongoClient().db.collection
    yield collection


@pytest.fixture
def dict_repo(collection):
    repo = DictRepo(collection)
    yield repo


@pytest.fixture
def model_repo(collection):
    repo = ModelRepo(collection)
    yield repo


def test_create_repo_with_unexpected_model_type(collection):
    with pytest.raises(ValueError):
        IntRepo(collection)


def test_count(collection, dict_repo):
    _insert_documents(collection, 3)
    assert dict_repo.count() == 3


def test_delete_all(collection, dict_repo):
    _insert_documents(collection, 3)
    dict_repo.delete_all()
    assert dict_repo.count() == 0


def test_delete_all_by_id(collection, dict_repo):
    ids = _insert_documents(collection, 3)
    dict_repo.delete_all_by_id(ids[0:2])
    assert dict_repo.count() == 1


def test_delete_by_id(collection, dict_repo):
    ids = _insert_documents(collection, 3)
    dict_repo.delete_by_id(ids[0])
    assert dict_repo.count() == 2


def test_exists_by_id(collection, dict_repo):
    ids = _insert_documents(collection, 3)
    assert dict_repo.exists_by_id(ids[0])


def test_find_all_dict_type(collection, dict_repo):
    _insert_documents(collection, 3)
    assert len(dict_repo.find_all()) == 3


def test_find_all_pydantic_model_type(collection, model_repo):
    _insert_documents(collection, 3)
    assert len(model_repo.find_all()) == 3


def test_find_page_dict_type(collection, dict_repo):
    _insert_documents(collection, 3)
    res = dict_repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_page_pydantic_model_type(collection, model_repo):
    _insert_documents(collection, 3)
    res = model_repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_all_by_id_dict_type(collection, dict_repo):
    ids = _insert_documents(collection, 3)
    assert len(dict_repo.find_all_by_id(ids[0:2])) == 2


def test_find_all_by_id_pydantic_model_type(collection, model_repo):
    ids = _insert_documents(collection, 3)
    assert len(model_repo.find_all_by_id(ids[0:2])) == 2


def test_find_by_id_dict_type(collection, dict_repo):
    ids = _insert_documents(collection, 3)
    assert dict_repo.find_by_id(ids[0])["value"] == "value 0"


def test_find_by_id_pydantic_model_type(collection, model_repo):
    ids = _insert_documents(collection, 3)
    assert model_repo.find_by_id(ids[0]).value == "value 0"


def test_save_dict_type(collection, dict_repo):
    res = dict_repo.save({"value": "value 0"})
    assert "_id" in res and res["value"] == "value 0"

    res["value"] = "value 1"
    res = dict_repo.save(res)
    assert res["value"] == "value 1"


def test_save_pydantic_model_type(collection, model_repo):
    res = model_repo.save(TestModel(value="value 0"))
    assert res.id is not None and res.value == "value 0"

    res.value = "value 1"
    res = model_repo.save(res)
    assert res.value == "value 1"


def _insert_documents(collection, size):
    return [collection.insert_one({"value": f"value {i}"}).inserted_id for i in range(size)]
