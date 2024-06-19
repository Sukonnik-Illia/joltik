from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from joltik.models.contacts import ContactsModel
    from joltik.models.customers import CustomerModel

from joltik.models.database import CrmBase


class InteractionsModel(CrmBase):
    __tablename__ = "interactions"
    date: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()

    customer: Mapped[CustomerModel] = relationship(back_populates="interactions", uselist=False)
    customer_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"))

    contacts: Mapped[list[ContactsModel]] = relationship(
        back_populates="interactions",
        uselist=True,
        secondary="interactions_contacts",
    )


class InteractionContacts(CrmBase):
    __tablename__ = "interactions_contacts"
    interactions_fk: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interactions.id"),
    )
    contacts_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id"))
