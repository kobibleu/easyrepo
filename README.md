# EasyRepo
Simple and flexible repository pattern implementation for Python.

This library provides interfaces that you can use to implement your own repository or simply using one of specific 
repository provided.

### Interfaces

- `CRUDRepository` is an interface for generic CRUD operations for a specific type.
  
  ```python
  from easyrepo import CRUDRepository
  
  class MyRepo(CRUDRepository[dict, int]):
    # ... implement abstract methods
  ```  
  
- `PagingRepository` adds additional method to ease paginated access to data.

  ```python
  from easyrepo import PagingRepository
  
  class MyRepo(PagingRepository[dict, int]):
    # ... implement abstract methods
  ```

### Repositories

- `MemoryRepository`: simplest usage of repository implementing `PagingRepository`, suited for rapid bootstrapping and prototyping.

  ```python
  from easyrepo import MemoryRepository
  
  test_repo = MemoryRepository()
  ```
  
- `MongoRepository`: mongo specific repository implementing `PagingRepository`.

  ```python
  from easyrepo import MongoRepository
  from pymongo import MongoClient
  
  client = MongoClient()
  db = client.test_database
  collection = db.test_collection
  
  test_repo = MongoRepository(collection=collection)
  ```


