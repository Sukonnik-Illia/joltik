from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from joltik.models.database import CrmBase

if TYPE_CHECKING:
    from joltik.models.deals import Deals

Service = Literal["SEO", "PPC", "SMM", "Creatives"]


class Services(CrmBase):
    __tablename__ = "services"
    service_type: Mapped[Service]
    description: Mapped[str] = mapped_column(nullable=False)
    deals: Mapped[list[Deals]] = relationship(back_populates="service", uselist=True)
