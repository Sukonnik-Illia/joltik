from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from joltik.errors import EntityDoesNotExistError
from joltik.models import Contacts, Customers, Deals, Services
from joltik.models.deals import Deal_stage, Deal_type
from joltik.session import DBAsyncSession

router = APIRouter()


class DealCreate(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    deal_name: str
    deal_type: Deal_type
    stage: Deal_stage
    ammount: int
    comments: str | None = None
    contact_fk: UUID
    service_fk: UUID
    customer_fk: UUID


class DealUpdate(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    deal_name: str | None = None
    deal_type: Deal_type | None = None
    stage: Deal_stage | None = None
    ammount: int | None = None
    comments: str | None = None
    contact_fk: UUID | None = None
    service_fk: UUID | None = None
    customer_fk: UUID | None = None


class DealResponse(DealCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: UUID


@router.get("/")
async def list_all_deals(db: DBAsyncSession) -> List[DealResponse]:
    result = await db.execute(
        select(Deals).options(
            selectinload(Deals.customer),
            selectinload(Deals.contact),
            selectinload(Deals.service),
        ),
    )
    return result.scalars().all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_deal(deal: DealCreate, db: DBAsyncSession) -> DealResponse:
    customer = await db.execute(select(Customers).filter(Customers.id == deal.customer_fk))
    customer = customer.scalars().first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    contact = await db.execute(
        select(Contacts)
        .options(selectinload(Contacts.customer))
        .filter(Contacts.id == deal.contact_fk),
    )
    contact = contact.scalars().first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if contact.customer_fk != deal.customer_fk:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more contacts do not belong to the specified customer",
        )

    service = await db.execute(select(Services).filter(Services.id == deal.service_fk))
    service = service.scalars().first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    new_deal_dict = deal.model_dump(mode="json")
    new_deal_sqla = Deals(**new_deal_dict)
    db.add(new_deal_sqla)
    await db.commit()
    await db.refresh(new_deal_sqla)

    await new_deal_sqla.awaitable_attrs.customer
    await new_deal_sqla.awaitable_attrs.contact
    await new_deal_sqla.awaitable_attrs.service

    return new_deal_sqla


@router.get("/{deal_id}")
async def select_deal(deal_id: UUID, db: DBAsyncSession) -> DealResponse:
    result = await db.execute(
        select(Deals)
        .options(
            selectinload(Deals.customer),
            selectinload(Deals.contact),
            selectinload(Deals.service),
        )
        .filter(Deals.id == deal_id),
    )
    deal = result.scalars().first()
    if not deal:
        raise EntityDoesNotExistError
    return deal


@router.put("/{deal_id}")
async def update_deal(
    deal_id: UUID,
    updated_deal_pyd: DealUpdate,
    db: DBAsyncSession,
) -> DealResponse:
    result = await db.execute(
        select(Deals)
        .options(
            selectinload(Deals.customer),
            selectinload(Deals.contact),
            selectinload(Deals.service),
        )
        .filter(Deals.id == deal_id),
    )
    deal_sqla = result.scalars().first()
    if not deal_sqla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    update_deal_dict = updated_deal_pyd.model_dump(mode="json", exclude_unset=True)

    if "service_fk" in update_deal_dict:
        service = await db.execute(
            select(Services).filter(Services.id == update_deal_dict["service_fk"]),
        )
        service = service.scalars().first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    if "customer_fk" in update_deal_dict:
        customer = await db.execute(
            select(Customers).filter(Customers.id == update_deal_dict["customer_fk"]),
        )
        customer = customer.scalars().first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        if "contact_fk" not in update_deal_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact update required when change customer",
            )

    if "contact_fk" in update_deal_dict:
        contact = await db.execute(
            select(Contacts)
            .options(selectinload(Contacts.customer))
            .filter(Contacts.id == update_deal_dict["contact_fk"]),
        )
        contact = contact.scalars().first()
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

        if (
            "customer_fk" in update_deal_dict
            and contact.customer_fk != updated_deal_pyd.customer_fk
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer does not have the specified contact",
            )

        if "customer_fk" not in update_deal_dict and contact.customer_fk != deal_sqla.customer_fk:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact does not belong to the specified customer",
            )

    for key, value in update_deal_dict.items():
        setattr(deal_sqla, key, value)

    await db.commit()
    await db.refresh(deal_sqla)
    return deal_sqla


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(deal_id: UUID, db: DBAsyncSession) -> None:
    deal = await db.get(Deals, deal_id)
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    await db.delete(deal)
    await db.commit()
