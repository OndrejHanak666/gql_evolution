from typing import Optional
import sqlalchemy
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .BaseModel import BaseModel, UUIDFKey, IDType


class PublicationModel(BaseModel):
    __tablename__ = "publications"

    id: Mapped[IDType] = mapped_column(primary_key=True, default=None, nullable=True)

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    published_date: Mapped[Optional[sqlalchemy.sql.sqltypes.DateTime]] = mapped_column(DateTime, default=None, nullable=True)
    reference: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    valid: Mapped[Optional[bool]] = mapped_column(Boolean, default=None, nullable=True)
    place: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)

    publication_type_id: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="ID of the publication type")

    created: Mapped[Optional[sqlalchemy.sql.sqltypes.DateTime]] = mapped_column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange: Mapped[Optional[sqlalchemy.sql.sqltypes.DateTime]] = mapped_column(
        DateTime,
        server_default=sqlalchemy.sql.func.now(),
        server_onupdate=sqlalchemy.sql.func.now()
    )

    createdby: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="who's created the entity")
    changedby: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="who's changed the entity")
    rbacobject: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="user or group id, determines access")