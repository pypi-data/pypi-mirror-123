from pydantic import BaseModel, Field, validator


class BaseSchema(BaseModel):
    pass


__all__ = [
    BaseSchema,
    Field,
    validator,
]
