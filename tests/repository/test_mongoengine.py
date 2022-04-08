import pytest
from mongoengine import Document, connect, disconnect, StringField

from easyrepo.model.paging import PageRequest
from easyrepo.model.sorting import Sort, Direction
from easyrepo.repository.mongoengine import MongoEngineRepository


class TestModel(Document):
    value: str = StringField(required=True)


class TestRepo(MongoEngineRepository[TestModel]):
    pass


class IntRepo(MongoEngineRepository[int]):
    pass


@pytest.fixture
def connection():
    connect("mongoenginetest", host="mongomock://localhost")
    yield
    disconnect()


@pytest.fixture
def repo(connection):
    repo = TestRepo()
    yield repo


def test_create_repo_with_unexpected_model_type():
    with pytest.raises(ValueError):
        IntRepo()


def test_count(repo):
    _insert_documents(3)
    assert repo.count() == 3


def test_delete_all(repo):
    _insert_documents(3)
    repo.delete_all()
    assert repo.count() == 0


def test_delete_all_by_id(repo):
    ids = _insert_documents(3)
    repo.delete_all_by_id(ids[0:2])
    assert repo.count() == 1


def test_delete_by_id(repo):
    ids = _insert_documents(3)
    repo.delete_by_id(ids[0])
    assert repo.count() == 2


def test_exists_by_id(repo):
    ids = _insert_documents(3)
    assert repo.exists_by_id(ids[0])


def test_find_all(repo):
    _insert_documents(3)
    assert len(repo.find_all()) == 3

    res = repo.find_all(Sort.by("value", direction=Direction.DES))
    assert [r.value for r in res] == ["value 2", "value 1", "value 0"]


def test_find_page(repo):
    _insert_documents(3)
    res = repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_all_by_id(repo):
    ids = _insert_documents(3)
    assert len(repo.find_all_by_id(ids[0:2])) == 2


def test_find_by_id(repo):
    ids = _insert_documents(3)
    assert repo.find_by_id(ids[0]).value == "value 0"


def test_save_unexpected_type(repo):
    with pytest.raises(ValueError):
        repo.save(1)


def test_save(repo):
    model = TestModel(value="value 0")
    model = repo.save(model)
    assert model.id is not None

    model.value = "value 1"
    model = repo.save(model)
    assert model.value == "value 1"


def test_save_all(repo):
    res = repo.save_all([
        TestModel(value="value 0"),
        TestModel(value="value 1"),
        TestModel(value="value 2")
    ])
    assert len(res) == 3
    assert len(repo.find_all()) == 3


def _insert_documents(size):
    return [TestModel(value=f"value {i}").save().reload().id for i in range(size)]
