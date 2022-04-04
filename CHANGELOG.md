# Change Log
All notable changes to this project will be documented in this file.

## 0.3.0

### Added

- Add `MongoEngineRepository` implementing `PagingRepository` interface.

## 0.2.2

### Added

- Add possibility to use pydantic model for `MongoRepository` typing.

## 0.2.1

### Added

- Add possibility to use pydantic model for `MemoryRepository` typing.

## 0.2.0

### Added

- Add `MemoryRepository` implementing `PagingRepository` interface.

## 0.1.0

### Added

- Add `CRUDRepository` interface.
- Add `PagingRepository` interface extending `CRUDRepository`.
- Add `Paging` and `Sorting` model.
- Add `MongoRepository` implementing `PagingRepository` interface.
