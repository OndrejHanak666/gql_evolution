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

    path_attribute_name = "path"
    parent_attribute_name = "mastertype"
    parent_id_attribute_name = "mastertype_id"
    children_attribute_name = "subtypes"


    path: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True, default=None, comment="Materialized path technique, not implemented")
    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    category_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("publicationcategories.id"), default=None, nullable=True, index=True, comment="ID of the associated category")
    mastertype_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("publicationtypes.id"), default=None, nullable=True, index=True, comment="ID of the master publication type for hierarchical structure")

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
    


    mastertype = relationship(
        "PublicationTypeModel",
        back_populates="subtypes",
        remote_side="PublicationTypeModel.id",
        uselist=False,
        viewonly=True
    )


    subtypes = relationship(
        "PublicationTypeModel",
        back_populates="mastertype",
        uselist=True,
        init=True,
        cascade="save-update"
    )

    