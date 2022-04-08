from typing import Optional

import bson
from pydantic import BaseModel


class ObjectId(bson.ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, bson.ObjectId):
            raise TypeError('ObjectId required')
        return bson.ObjectId(v)


class Document(BaseModel):
    id: Optional[ObjectId]
