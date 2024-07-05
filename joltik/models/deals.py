from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from joltik.models.contacts import Contacts
    from joltik.models.customers import Customers
    from joltik.models.services import Services

from joltik.models.database import CrmBase

Deal_type = Literal["New business", "Existing Business"]
Deal_stage = Literal["Prospecting", "Qualified", "Negotiation", "Won", "Lost"]


class Deals(CrmBase):
    __tablename__ = "deals"
    deal_name: Mapped[str] = mapped_column(nullable=False)
    deal_type: Mapped[Deal_type]
    stage: Mapped[Deal_stage]
    ammount: Mapped[int] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column()

    contact: Mapped[Contacts] = relationship(back_populates="deals", uselist=False)
    contact_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id"))

    service: Mapped[Services] = relationship(back_populates="deals", uselist=False)
    service_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("services.id"))

    customer: Mapped[Customers] = relationship(back_populates="deals", uselist=False)
    customer_fk: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"))
