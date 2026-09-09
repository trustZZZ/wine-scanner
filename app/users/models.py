from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import String, ForeignKey, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_age_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class AgeVerification(Base):
    __tablename__ = "age_verifications"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    raw_response: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="queued")
    ocr_raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    matched_wine_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("wines.id"), nullable=True)
    # ДОБАВИТЬ ЭТИ ДВА ПОЛЯ:
    wine_card: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float | None] = mapped_column(nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
