from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from joltik.models.contacts import ContactsModel
    from joltik.models.customers import CustomerModel
    from joltik.models.services import ServicesModel

from joltik.models.database import CrmBase

Deal_type = Literal["New business", "Recurring services", "New to excisting client"]
Deal_stage = Literal["Connect", "Propose", "Win", "Lose"]


class DealsModel(CrmBase):
    __tablename__ = "deals"
    deal_name: Mapped[str] = mapped_column(nullable=False)
    deal_type = Mapped[Deal_type]
    stage = Mapped[Deal_stage]
    ammount: Mapped[int] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column()

    contact: Mapped[ContactsModel] = relationship(back_populates="deals", uselist=False)
    contact_fk: Mapped[int] = mapped_column(ForeignKey("contact_persons.id"), nullable=False)

    service: Mapped[ServicesModel] = relationship(back_populates="deals", uselist=False)
    service_fk: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)

    customer: Mapped[CustomerModel] = relationship(back_populates="deals", uselist=False)
    customer_fk: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
