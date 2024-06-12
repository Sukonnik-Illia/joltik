from typing import Literal

from models.database import CrmBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

Deal_type = Literal["New business", "Recurring services", "New to excisting client"]
Deal_stage = Literal["Connect", "Propose", "Win", "Lose"]


class DealsModel(CrmBase):
    __tablename__ = "deals"
    deal_name: Mapped[str] = mapped_column(nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    responcible_customer: Mapped[int] = mapped_column(
        ForeignKey("contact_persons.id"),
        nullable=False,
    )
    service: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    deal_type = Mapped[Deal_type]
    stage = Mapped[Deal_stage]
    ammount: Mapped[int] = mapped_column(nullable=False)
    comments: Mapped[str] = mapped_column()
