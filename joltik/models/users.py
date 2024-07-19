from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from joltik.models.database import CrmBase

if TYPE_CHECKING:
    from joltik.models.user_roles import Role


class User(CrmBase):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
    role: Mapped[Role] = relationship(back_populates="users", uselist=False)
    role_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("role.id"))
    # Mandatory fields from fastapi-users model
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
