from typing import Optional
import sqlalchemy
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
)

from .BaseModel import BaseModel, UUIDFKey, IDType


class PublicationModel(BaseModel):
    __tablename__ = "publications"

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    published_date: Mapped[Optional[sqlalchemy.sql.sqltypes.DateTime]] = mapped_column(DateTime, default=None, nullable=True)
    reference: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    valid: Mapped[Optional[bool]] = mapped_column(Boolean, default=None, nullable=True)
    place: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)

    publication_type_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("publicationtypes.id"), default=None, nullable=True, comment="ID of the publication type")

    # vztah na autory publikace (odpovídá PublicationAuthorModel)
    authors = relationship(
        "PublicationAuthorModel",
         back_populates="publication",
         uselist=True,
         init=True,
         cascade="save-update"
     )
    
    # vztah na typ publikace (odpovídá PublicationTypeModel)
    publicationtype = relationship(
        "PublicationTypeModel",
         back_populates="publications",
         viewonly=True,
         uselist=False
     )  