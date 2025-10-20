from typing import Optional
import sqlalchemy
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDFKey, IDType


class PublicationTypeModel(BaseModel):
    __tablename__ = "publicationtypes"

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    category_id: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="ID of the associated category")

    