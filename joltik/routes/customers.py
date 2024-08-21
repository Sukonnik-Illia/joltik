from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.models import Customers
from joltik.models.customers import LeadStatus

router = APIRouter()


class CustomerCreate(BaseModel):
    company_name: str
    industry: str
    address: str
    email: str
    phone_number: str
    lead_status: LeadStatus

    class Config:
        from_attributes = True


class CustomerResponse(CustomerCreate):
    id: UUID


@router.get("/")
def list_all(db: Session = Depends(get_db)) -> list[CustomerResponse]:
    return db.query(Customers).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)) -> CustomerResponse:
    new_customer = Customers(**jsonable_encoder(customer))
    db.add(new_customer)
    db.commit()
    return new_customer


# {
#   "company_name": "Butonchik",
#   "industry": "insulation",
#   "address": "Farfaraway str",
#   "email": "figulka@butonchik.com",
#   "phone_number": "000",
#   "lead_status": "Proposal"
# }


@router.get("/{customer_id}", response_model=CustomerResponse)
def list_one(customer_id: UUID, db: Session = Depends(get_db)) -> CustomerResponse:
    customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return customer


@router.put("/{customer_id}", status_code=status.HTTP_202_ACCEPTED)
def update_customer(
    customer_id: UUID,
    customer_update: CustomerCreate,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_data = customer_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)) -> None:
    customer = db.query(Customers).filter(Customers.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(customer)
    db.commit()
