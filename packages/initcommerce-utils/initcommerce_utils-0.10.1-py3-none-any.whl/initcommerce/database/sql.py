# from sqlalchemy.ext.asyncio import AsyncSession as Session
# from sqlalchemy.ext.asyncio import create_async_engine as _create_engine
from sqlalchemy import (  # noqa: F401
    JSON,
    BigInteger,
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (  # noqa: F401
    Session,
    declarative_mixin,
    relationship,
    sessionmaker,
)

from initcommerce.common.uuid import UUID

# HACK: enforce singleton
_conn: Session = None


def get_db(db_uri: str):
    global _conn

    engine = _create_engine(db_uri)

    if _conn is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
        _conn = SessionLocal()

    return _conn


BaseDBModel = declarative_base()


@declarative_mixin
class PrimaryIDMixin:
    id = Column(
        BigInteger, primary_key=True, autoincrement=False, default=UUID.fetch_one
    )


@declarative_mixin
class IndexedIDMixin:
    id = Column(BigInteger, index=True, default=UUID.fetch_one)
