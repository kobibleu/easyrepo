import pytest
from mongomock import MongoClient

from easyrepo.model.paging import PageRequest
from easyrepo.repository.mongo import MongoRepository


@pytest.fixture
def collection():
    collection = MongoClient().db.collection
    yield collection


@pytest.fixture
def repo(collection):
    repo = MongoRepository(collection)
    yield repo


def test_count(collection, repo):
    _insert_documents(collection, 3)
    assert repo.count() == 3


def test_delete_all(collection, repo):
    _insert_documents(collection, 3)
    repo.delete_all()
    assert repo.count() == 0


def test_delete_all_by_id(collection, repo):
    ids = _insert_documents(collection, 3)
    repo.delete_all_by_id(ids[0:2])
    assert repo.count() == 1


def test_delete_by_id(collection, repo):
    ids = _insert_documents(collection, 3)
    repo.delete_by_id(ids[0])
    assert repo.count() == 2


def test_exists_by_id(collection, repo):
    ids = _insert_documents(collection, 3)
    assert repo.exists_by_id(ids[0])


def test_find_all(collection, repo):
    _insert_documents(collection, 3)
    assert len(repo.find_all()) == 3


def test_find_page(collection, repo):
    _insert_documents(collection, 3)
    res = repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_all_by_id(collection, repo):
    ids = _insert_documents(collection, 3)
    assert len(repo.find_all_by_id(ids[0:2])) == 2


def test_find_by_id(collection, repo):
    ids = _insert_documents(collection, 3)
    assert repo.find_by_id(ids[0])["value"] == "value 0"


def test_save(collection, repo):
    res = repo.save({"value": "value 0"})
    assert "_id" in res and res["value"] == "value 0"

    res["value"] = "value 1"
    res = repo.save(res)
    assert res["value"] == "value 1"


def _insert_documents(collection, size):
    return [collection.insert_one({"value": f"value {i}", "deleted": False}).inserted_id for i in range(size)]
