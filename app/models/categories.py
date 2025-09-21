"""カテゴリーの ORM モデル定義

- DB 上の id は UUID 型 (PostgreSQL) で保存されているため
    SQLAlchemy の UUID 型(as_uuid=True) を利用します。
"""

import uuid

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
