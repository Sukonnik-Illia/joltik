from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from joltik.models.customers import Customer
    from joltik.models.deals import Deals
    from joltik.models.interactions import Interactions

from joltik.models.database import CrmBase
from joltik.models.interactions import InteractionContacts


class Contacts(CrmBase):
    __tablename__ = "contacts"
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    job_title: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()

    customer: Mapped[Customer] = relationship(back_populates="contacts", uselist=False)
    customer_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"))
    deals: Mapped[list[Deals]] = relationship(back_populates="contact", uselist=True)
    interactions: Mapped[list[Interactions]] = relationship(
        back_populates="contacts",
        uselist=True,
        secondary=InteractionContacts.__tablename__,
    )
