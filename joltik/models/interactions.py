from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from joltik.models.database import CrmBase


class InteractionsModel(CrmBase):
    __tablename__ = "interactions"
    contact_person_id: Mapped[int] = mapped_column(ForeignKey("contact_persons.id"))
    date: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
