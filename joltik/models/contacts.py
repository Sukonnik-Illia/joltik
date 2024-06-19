from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from joltik.models.customers import CustomerModel
    from joltik.models.deals import DealsModel
    from joltik.models.interactions import InteractionsModel

from joltik.models.database import CrmBase
from joltik.models.interactions import InteractionContacts


class ContactsModel(CrmBase):
    __tablename__ = "contacts"
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    job_title: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()

    customer: Mapped[CustomerModel] = relationship(back_populates="contacts", uselist=False)
    customer_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"))
    deals: Mapped[list[DealsModel]] = relationship(back_populates="contact", uselist=True)
    interactions: Mapped[list[InteractionsModel]] = relationship(
        back_populates="contacts",
        uselist=True,
        secondary=InteractionContacts.__tablename__,
    )
