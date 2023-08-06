import abc

from pydantic import BaseConfig, BaseModel, Field, validator  # noqa: F401

from initcommerce.common.value_object import ID


class BaseEntity(BaseModel, metaclass=abc.ABCMeta):
    id: int = Field(default_factory=ID.fetch_one)

    class Config(BaseConfig):
        orm_mode = True
