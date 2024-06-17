from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from joltik.models.database import CrmBase

if TYPE_CHECKING:
    from joltik.models.services import ServicesModel

Service = Literal["SEO", "PPC", "SMM", "Creatives"]


class ServicesModel(CrmBase):
    __tablename__ = "services"
    service_type: Mapped[Service]
    description: Mapped[str] = mapped_column(nullable=False)
    deals: Mapped[list[ServicesModel]] = relationship(back_populates="service", uselist=True)
