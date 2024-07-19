from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from joltik.models.database import CrmBase

if TYPE_CHECKING:
    from joltik.models.users import User

UserRoles = Literal["Mortal", "Admin"]


class Role(CrmBase):
    __tablename__ = "role"
    user_role: Mapped[UserRoles] = mapped_column(unique=True)
    users: Mapped[list[User]] = relationship(back_populates="role", uselist=True)
