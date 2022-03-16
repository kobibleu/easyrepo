from enum import Enum
from typing import List, Optional, ClassVar

from pydantic import BaseModel, Field


class Direction(Enum):
    """
    Enumeration for sort directions.
    """
    ASC = 1
    DES = -1

    def is_ascending(self):
        return self.name == Direction.ASC.name

    def is_descending(self):
        return self.name == Direction.DES.name

    @staticmethod
    def value_of(name: str) -> Optional["Direction"]:
        for d in Direction:
            if d.name == name:
                return d
        return None

    @staticmethod
    def values() -> List["Direction"]:
        return [d for d in Direction]


class Order(BaseModel):
    """
    PropertyPath implements the pairing of a Sort.Direction and a property.
    """
    key: str
    direction: Direction


class Sort(BaseModel):
    """
    Sort option for queries.
    """
    DEFAULT_DIRECTION: ClassVar[Direction] = Direction.ASC

    orders: List[Order] = Field(default_factory=lambda: [])

    @classmethod
    def by(cls, *keys: str, direction: Direction = DEFAULT_DIRECTION) -> "Sort":
        """
        Creates a new Sort for the given Orders.
        """
        orders = [Order(key=k, direction=direction) for k in keys]
        return Sort(orders=orders)

    def ascending(self) -> "Sort":
        """
        Returns a new Sort with the current setup but ascending order direction.
        """
        for order in self.orders:
            order.direction = Direction.ASC
        return self

    def descending(self) -> "Sort":
        """
        Returns a new Sort with the current setup but descending order direction.
        """
        for order in self.orders:
            order.direction = Direction.DES
        return self
