# app/models/wine.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4
from datetime import datetime
from uuid import UUID
from app.database import Base

class Wine(Base):
    __tablename__ = "wines"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    egais_id: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    producer: Mapped[str] = mapped_column(String, nullable=False)
    vintage_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region: Mapped[str | None] = mapped_column(String, nullable=True)
    grape_varieties: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    certificates: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    label_keywords: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Опционально: откуда пришла запись (из OCR-задачи)
    source_task_id: Mapped[UUID | None] = mapped_column(
    PGUUID(as_uuid=True),
    nullable=True,
    index=True,
)



