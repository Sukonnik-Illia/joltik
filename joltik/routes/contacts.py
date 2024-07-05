from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.models import Contacts, Customers

router = APIRouter()


class Customer(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    job_title: str
    email: str
    phone_number: str
    comment: str
    customer: Customer

    class Config:
        from_attributes = True


class ContactResponse(ContactCreate):
    id: UUID


class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    job_title: str | None = None
    email: str | None = None
    phone_number: str | None = None
    comment: str | None = None
    customer: Customer | None = None

    class Config:
        from_attributes = True


@router.get("/")
def list_contacts(db: Session = Depends(get_db)) -> list[ContactResponse]:
    return db.query(Contacts).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)) -> ContactResponse:
    customer = db.query(Customers).filter(Customers.id == contact.customer.id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    new_contact_dict = contact.model_dump(exclude={"customer"})
    new_contact_sqla = Contacts(**new_contact_dict, customer_fk=contact.customer.id)
    db.add(new_contact_sqla)
    db.commit()
    return new_contact_sqla


@router.get("/{contact_id}")
def list_one_contact(contact_id: UUID, db: Session = Depends(get_db)) -> ContactResponse:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.put("/{contact_id}", status_code=status.HTTP_202_ACCEPTED)
def update_contact(
    contact_id: UUID,
    updated_contact: ContactUpdate,
    db: Session = Depends(get_db),
) -> ContactResponse:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    update_data = updated_contact.model_dump(exclude_unset=True)

    if "customer" in update_data:
        customer = db.query(Customers).filter(Customers.id == update_data["customer"]["id"]).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        contact.customer_fk = update_data["customer"]["id"]
        del update_data["customer"]

    for key, value in update_data.items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: UUID, db: Session = Depends(get_db)) -> None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(contact)
    db.commit()
