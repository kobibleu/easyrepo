# EasyRepo
Simple and flexible repository pattern implementation for Python.

This library provides interfaces that you can use to implement your own repository or simply using one of specific 
repository provided.

### Interfaces

- `CRUDRepository` is an interface for generic CRUD operations for a specific type.
  
  ```python
  from easyrepo import CRUDRepository
  
  class MyRepo(CRUDRepository):
    # ... implement abstract methods
  ```  
  
- `PagingRepository` adds additional method to ease paginated access to data.

  ```python
  from easyrepo import PagingRepository
  
  class MyRepo(PagingRepository):
    # ... implement abstract methods
  ```

### Repositories

- `MemoryRepository`: simplest usage of repository implementing `PagingRepository`, suited for rapid bootstrapping and prototyping.

  ```python
  from easyrepo.repository.memory import MemoryRepository
  
  
  class MyRepo(MemoryRepository[dict]):
    pass
  
  
  test_repo = MyRepo()
  ```
  
- `MongoRepository`: mongo specific repository implementing `PagingRepository`.

  ```python
  from easyrepo.repository.mongo import MongoRepository
  from pymongo import MongoClient
  
  
  class MyRepo(MongoRepository[dict]):
    pass
  
  
  client = MongoClient()
  db = client.test_database
  collection = db.test_collection
  
  test_repo = MyRepo(collection=collection)
  ```
  
- `MongoEngineRepository`: dedicated repository for MongoEngine ODM implementing `PagingRepository`.

  ```python
  from easyrepo.repository.mongoengine import MongoEngineRepository
  from mongoengine import Document, StringField
  
  
  class TestModel(Document):
    value: str = StringField(required=True)
  
  
  class MyRepo(MongoEngineRepository[TestModel]):
    pass
  
  
  test_repo = MyRepo()
  ```
  
- `SqlRepository`: dedicated repository for SQLAlchemy ORM implementing `PagingRepository`.

  ```python
  from easyrepo.repository.sql import SqlRepository
  from easyrepo.model.sql import Entity
  from sqlalchemy import create_engine, Column, Integer, String
  from sqlalchemy.orm import sessionmaker
  
  
  class TestModel(Entity):
    id = Column(Integer, primary_key=True, index=True)
    value: str = Column(String, nullable=False)
  
  
  class MyRepo(SqlRepository[TestModel]):
    pass
  
  
  engine = create_engine(SQLALCHEMY_DATABASE_URI)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  session = SessionLocal()
  test_repo = MyRepo(session)
  ```


