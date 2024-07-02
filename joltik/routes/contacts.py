from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.models import Contacts

router = APIRouter()


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    job_title: str
    email: str
    phone_number: str
    comment: str
    customer_fk: UUID

    class Config:
        from_attributes = True


class ContactResponse(ContactCreate):
    id: UUID


@router.get("/")
def list_all(db: Session = Depends(get_db)) -> list[ContactResponse]:
    return db.query(Contacts).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)) -> ContactResponse:
    new_contact = Contacts(**jsonable_encoder(contact))
    db.add(new_contact)
    db.commit()
    return new_contact


@router.get("/{contact_id}")
def list_one(contact_id: UUID, db: Session = Depends(get_db)) -> ContactResponse:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


# @router.put("/{contact_id}", status_code=status.HTTP_202_ACCEPTED)
# def update_contact(
#     contact_id: UUID,
#     contact_update: ContactCreate,
#     db: Session = Depends(get_db),
# ) -> ContactResponse:
#     contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     update_data = contact_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(customer, key, value)
#     db.commit()
#     db.refresh(customer)
#     return customer


@router.delete("/{contact_id}")
def delete_contact(contact_id: UUID, db: Session = Depends(get_db)) -> None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(contact)
    db.commit()
