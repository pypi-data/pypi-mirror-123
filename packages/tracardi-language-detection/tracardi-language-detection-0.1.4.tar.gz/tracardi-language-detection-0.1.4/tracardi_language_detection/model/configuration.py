from typing import Optional

from pydantic import BaseModel, validator
from tracardi.domain.entity import Entity


class Key(BaseModel):
    token: str

    @validator("token")
    def must_not_be_empty(cls, value):
        if len(value) < 1:
            raise ValueError("Token must not be empty.")
        return value


class Configuration(BaseModel):
    source: Entity
    message: str
    timeout: Optional[float] = 15

    @validator("message")
    def must_not_be_empty(cls, value):
        if len(value) < 2:
            raise ValueError("Message must not be empty.")
        return value
