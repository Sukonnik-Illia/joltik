from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
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
    customer_fk: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    contacts: Mapped[list[ContactsModel]] = relationship(
        back_populates="interactions",
        uselist=True,
        secondary="interactions_contacts",
    )


class InteractionContacts(CrmBase):
    __table__ = "interactions_contacts"
    interactions_fk: Mapped[int] = mapped_column(ForeignKey("interactions.id"))
    contacts_fk: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
