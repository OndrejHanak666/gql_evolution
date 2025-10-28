from typing import Optional
import sqlalchemy
from sqlalchemy import Integer, Float, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDFKey, IDType


class PublicationCategoryModel(BaseModel):
    __tablename__ = "publicationcategories"

    name: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)
    name_en: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True)