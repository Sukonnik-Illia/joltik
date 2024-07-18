from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from joltik.db import DBAsyncSession
from joltik.models import Customers
from joltik.models.customers import LeadStatus

router = APIRouter()


class CustomerCreate(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    company_name: str
    industry: str
    address: str
    email: str
    phone_number: str
    lead_status: LeadStatus


class CustomerResponse(CustomerCreate):
    id: UUID


@router.get("/")
async def list_all_customers(db: DBAsyncSession) -> list[CustomerResponse]:
    result = await db.execute(select(Customers))
    return result.scalars().all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(customer_pyd: CustomerCreate, db: DBAsyncSession) -> CustomerResponse:
    new_customer_sqla = Customers(**jsonable_encoder(customer_pyd))
    db.add(new_customer_sqla)
    await db.commit()
    await db.refresh(new_customer_sqla)
    return new_customer_sqla


# {
#   "company_name": "Butonchik",
#   "industry": "insulation",
#   "address": "Farfaraway str",
#   "email": "figulka@butonchik.com",
#   "phone_number": "000",
#   "lead_status": "Proposal"
# }


@router.get("/{customer_id}", response_model=CustomerResponse)
async def select_customer(customer_id: UUID, db: DBAsyncSession) -> CustomerResponse:
    customer = await db.get(Customers, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@router.put("/{customer_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer(
    customer_id: UUID,
    updated_customer_pyd: CustomerCreate,
    db: DBAsyncSession,
) -> CustomerResponse:
    customer_sqla = await db.get(Customers, customer_id)
    if not customer_sqla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    update_customer_dict = updated_customer_pyd.model_dump(mode="json", exclude_unset=True)
    for key, value in update_customer_dict.items():
        setattr(customer_sqla, key, value)
    await db.commit()
    await db.refresh(customer_sqla)
    return customer_sqla


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: UUID, db: DBAsyncSession) -> None:
    customer_sqla = await db.get(Customers, customer_id)
    if customer_sqla is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(customer_sqla)
    await db.commit()
