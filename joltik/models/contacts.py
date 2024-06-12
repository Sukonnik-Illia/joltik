from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from joltik.models.database import CrmBase


class ContactsModel(CrmBase):
    __tablename__ = "contact_persons"
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    job_title: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column()
    comment: Mapped[str] = mapped_column()
