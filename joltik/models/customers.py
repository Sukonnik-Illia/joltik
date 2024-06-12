from __future__ import annotations

import json
from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from joltik.models.database import CrmBase


def load_status_list(json_file: str) -> list[str]:
    with open(json_file) as file:
        data = json.load(file)
        return data["status_name"]


def create_dynamic_enum(name: str, values: list[str]) -> Enum:
    return Enum(name, {value.upper(): value for value in values})


lead_status_values = load_status_list("./joltik/models/lead_statuses.json")
LeadStatusEnum = create_dynamic_enum("LeadStatusEnum", lead_status_values)


class CustomerModel(CrmBase):
    __tablename__ = "customers"
    company_name: Mapped[int] = mapped_column(nullable=False)
    industry: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    lead_status: Mapped[Enum] = mapped_column(
        SQLAlchemyEnum(LeadStatusEnum),
        default=LeadStatusEnum.NEW,
        nullable=False,
    )
    # can be not working properly https://stackoverflow.com/questions/76268799/how-should-i-declare-enums-in-sqlalchemy-using-mapped-column-to-enable-type-hin
