from typing import Literal

from models.database import CrmBase
from sqlalchemy.orm import Mapped, mapped_column

Service = Literal["SEO", "PPC", "SMM", "Creatives"]


class ServicesModel(CrmBase):
    __tablename__ = "services"
    service_type: Mapped[Service]
    name: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
