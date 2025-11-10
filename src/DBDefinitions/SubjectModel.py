from typing import Optional
import sqlalchemy
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
)

from .BaseModel import BaseModel, UUIDFKey, IDType


class SubjectModel(BaseModel):
    __tablename__ = "publication_subjects"

    publication_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("publications.id"), default=None, nullable=True, comment="ID of the publication")
    subject_id: Mapped[Optional[IDType]] = mapped_column(ForeignKey("plan_subjects.id"), default=None, nullable=True, comment="ID of the subject")