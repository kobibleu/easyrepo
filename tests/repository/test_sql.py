import pytest
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import Column, Integer, String

from easyrepo.model.sql import SqlModel
from easyrepo.repository.sql import SqlRepository


class TestModel(SqlModel):
    id = Column(Integer, primary_key=True, index=True)
    value: str = Column(String, nullable=False)


class TestRepo(SqlRepository[TestModel]):
    pass


@pytest.fixture
def session():
    session = UnifiedAlchemyMagicMock()
    session.add(TestModel(id=1, value="value 1"))
    session.add(TestModel(id=2, value="value 2"))
    session.add(TestModel(id=3, value="value 3"))
    yield session


@pytest.fixture
def repo(session):
    repo = TestRepo(session)
    yield repo


def test_count(repo):
    assert repo.count() == 3


# def test_delete_all(repo):
#     repo.delete_all()
#     assert repo.count() == 0
#
#
# def test_delete_all_by_id(repo):
#     repo.delete_all_by_id((1, 2))
#     assert repo.count() == 1
#
#
# def test_delete_by_id(repo):
#     repo.delete_by_id(1)
#     assert repo.count() == 2
#
#
# def test_exists_by_id(repo):
#     assert repo.exists_by_id(1)
#     assert not repo.exists_by_id(4)
