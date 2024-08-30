from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from joltik.models import Contacts, Customers
from joltik.session import DBAsyncSession

router = APIRouter()


class Customer(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    id: UUID


class ContactCreate(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    job_title: str
    email: str
    phone_number: str
    comment: str
    customer: Customer


class ContactResponse(ContactCreate):
    id: UUID


class ContactUpdate(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    first_name: str | None = None
    last_name: str | None = None
    job_title: str | None = None
    email: str | None = None
    phone_number: str | None = None
    comment: str | None = None
    customer: Customer | None = None


@router.get("/")
async def list_all_contacts(db: DBAsyncSession) -> list[ContactResponse]:
    result = await db.execute(select(Contacts).options(selectinload(Contacts.customer)))
    return result.scalars().all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: DBAsyncSession) -> ContactResponse:
    result = await db.execute(select(Customers).filter(Customers.id == contact.customer.id))
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong customer id")
    new_contact_dict = contact.model_dump(mode="json", exclude={"customer"})
    new_contact_sqla = Contacts(**new_contact_dict, customer_fk=contact.customer.id)
    db.add(new_contact_sqla)
    await db.commit()
    await db.refresh(new_contact_sqla)
    await new_contact_sqla.awaitable_attrs.customer
    return ContactResponse.model_validate(new_contact_sqla)


# {
#   "first_name": "Vasya",
#   "last_name": "Pupkin",
#   "job_title": "no-doer",
#   "email": "vasyapupkin@butonchik.com",
#   "phone_number": "+8032",
#   "comment": "no-comment",
#   "customer": {"id": "7696bc4f-8165-4548-a1a9-6eeb124f4bf9"},
# }


@router.get("/{contact_id}")
async def select_contact(contact_id: UUID, db: DBAsyncSession) -> ContactResponse:
    result = await db.execute(
        select(Contacts).options(selectinload(Contacts.customer)).filter(Contacts.id == contact_id),
    )
    contact = result.scalars().first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return contact


@router.put("/{contact_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_contact(
    contact_id: UUID,
    updated_contact: ContactUpdate,
    db: DBAsyncSession,
) -> ContactResponse:
    result = await db.execute(
        select(Contacts).options(selectinload(Contacts.customer)).filter(Contacts.id == contact_id),
    )
    contact_sqla = result.scalars().first()
    if not contact_sqla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    update_data_dict = updated_contact.model_dump(mode="json", exclude_unset=True)

    if "customer" in update_data_dict:
        customer = await db.get(Customers, update_data_dict["customer"]["id"])
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong customer id")
        contact_sqla.customer_fk = update_data_dict["customer"]["id"]
        del update_data_dict["customer"]

    for key, value in update_data_dict.items():
        setattr(contact_sqla, key, value)
    await db.commit()
    await db.refresh(contact_sqla)
    return contact_sqla


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: UUID, db: DBAsyncSession) -> None:
    contact = await db.get(Contacts, contact_id)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(contact)
    await db.commit()
