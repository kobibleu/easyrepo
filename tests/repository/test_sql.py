import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session

from easyrepo.model.paging import PageRequest
from easyrepo.model.sorting import Sort, Direction
from easyrepo.model.sql import Entity
from easyrepo.repository.sql import SqlRepository


class TestModel(Entity):
    id = Column(Integer, primary_key=True, index=True)
    value: str = Column(String, nullable=False)


class TestRepo(SqlRepository[TestModel]):
    pass


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    session = Session(bind=engine)
    Entity.metadata.create_all(engine)
    session.add(TestModel(id=1, value="value 1"))
    session.add(TestModel(id=2, value="value 2"))
    session.add(TestModel(id=3, value="value 3"))
    session.commit()
    yield session


@pytest.fixture
def repo(session):
    repo = TestRepo(session)
    yield repo


def test_count(repo):
    assert repo.count() == 3


def test_delete_all(repo):
    repo.delete_all()
    assert repo.count() == 0


def test_delete_all_by_id(repo):
    repo.delete_all_by_id((1, 2))
    assert repo.count() == 1


def test_delete_by_id(repo):
    repo.delete_by_id(1)
    assert repo.count() == 2


def test_exists_by_id(repo):
    assert repo.exists_by_id(1)
    assert not repo.exists_by_id(4)


def test_find_all(repo):
    assert len(repo.find_all()) == 3

    res = repo.find_all(sort=Sort.by("value", direction=Direction.DES))
    assert [r.value for r in res] == ["value 3", "value 2", "value 1"]


def test_find_pag(repo):
    res = repo.find_page(PageRequest.of_size(2))
    assert len(res.content) == 2
    assert res.total_elements == 3


def test_find_all_by_id(repo):
    assert len(repo.find_all_by_id([1, 2])) == 2


def test_find_by_id(repo):
    assert repo.find_by_id(1).value == "value 1"
    assert repo.find_by_id(4) is None


def test_save_unexpected_type(repo):
    with pytest.raises(ValueError):
        repo.save(1)


def test_save(repo):
    res = repo.save(TestModel(value="value 4"))
    assert res.id == 4
    assert res.value == "value 4"

    res.value = "value 5"
    res = repo.save(res)
    assert res.value == "value 5"


def test_save_all(repo):
    model = repo.find_by_id(1)
    model.value = "value 4"
    res = repo.save_all([
        model,
        TestModel(value="value 5")
    ])
    assert len(res) == 2
    assert len(repo.find_all()) == 4
