from __future__ import annotations

# import json
from typing import TYPE_CHECKING, Literal

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from joltik.models.contacts import Contacts
    from joltik.models.deals import Deals
    from joltik.models.interactions import Interactions


from joltik.models.database import CrmBase

# def load_status_list(json_file: str) -> list[str]:
#     with open(json_file) as file:
#         data = json.load(file)
#         return data["status_name"]

# def create_dynamic_enum(name: str, values: list[str]) -> Enum:
#     return Enum(name, {value.upper(): value for value in values})
# lead_status_values = load_status_list("./joltik/models/lead_statuses.json")
# LeadStatusEnum = create_dynamic_enum("LeadStatusEnum", lead_status_values)

LeadStatus = Literal["New", "Connected", "Proposal", "Client", "Lost"]


class Customers(CrmBase):
    __tablename__ = "customers"
    company_name: Mapped[str] = mapped_column(nullable=False)
    industry: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    lead_status: Mapped[LeadStatus]

    contacts: Mapped[list[Contacts]] = relationship(back_populates="customer", uselist=True)
    deals: Mapped[list[Deals]] = relationship(back_populates="customer", uselist=True)
    interactions: Mapped[list[Interactions]] = relationship(
        back_populates="customer",
        uselist=True,
    )
