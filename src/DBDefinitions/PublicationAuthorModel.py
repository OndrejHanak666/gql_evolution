from typing import Optional
import sqlalchemy
from sqlalchemy import Integer, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .BaseModel import BaseModel, UUIDFKey, IDType


class PublicationAuthorModel(BaseModel):
    __tablename__ = "publication_authors"

    order: Mapped[Optional[int]] = mapped_column(Integer, default=None, nullable=True)
    share: Mapped[Optional[float]] = mapped_column(Float, default=None, nullable=True)

    publication_id: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="ID of the associated publication")
    user_id: Mapped[Optional[IDType]] = UUIDFKey(default=None, nullable=True, comment="ID of the associated user")

    

    # vztah na publikaci
    # publication = relationship(
    #     "PublicationModel",
    #     back_populates="authors",
    #     viewonly=True,
    #     uselist=False
    # )
