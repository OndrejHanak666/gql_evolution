from typing import Optional
import sqlalchemy
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
)

from .BaseModel import BaseModel, UUIDFKey, IDType


class PublicationTypeModel(BaseModel):
    __tablename__ = "publicationtypes"

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    category_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("publicationcategories.id"), default=None, nullable=True, comment="ID of the associated category")


    #vztah na publikace (odpovídá PublicationModel)
    publications = relationship(
        "PublicationModel",
         back_populates="publicationtype",
         uselist=True,
         init=True,
         cascade="save-update"
     )
    
    #vztah na kategorii publikace (odpovídá PublicationCategoryModel)
    category = relationship(
        "PublicationCategoryModel",
         back_populates="publicationtypes",
         viewonly=True,
         uselist=False
     )

    