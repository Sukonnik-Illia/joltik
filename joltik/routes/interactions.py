from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.errors import EntityDoesNotExistError
from joltik.models import Contacts, Customers, InteractionContacts, Interactions

router = APIRouter()


class Contact(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    date: int
    type: str
    description: str
    customer_fk: UUID
    contacts: List[Contact]

    class Config:
        from_attributes = True


class InteractionResponse(InteractionCreate):
    id: UUID


class InteractionUpdate(BaseModel):
    date: Union[int, None] = None
    type: Union[str, None] = None
    description: Union[str, None] = None
    customer_fk: Union[UUID, None] = None
    contacts: Union[List[Contact], None] = None

    class Config:
        from_attributes = True


# def from_interaction(interaction: Interactions, db: Session) -> InteractionResponse:
#     contact_ids = [
#         contact.contacts_fk
#         for contact in db.query(InteractionContacts)
#         .filter(InteractionContacts.interactions_fk == interaction.id)
#         .all()
#     ]
#     interaction_data = jsonable_encoder(interaction)
#     interaction_data["contacts"] = contact_ids
#     return InteractionResponse(**interaction_data)


@router.get("/", response_model=List[InteractionResponse])
def list_interactions(db: Session = Depends(get_db)) -> List[InteractionResponse]:
    return db.query(Interactions).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db),
) -> InteractionResponse:
    # Ensure the customer exists
    customer = db.query(Customers).filter(Customers.id == interaction.customer_fk).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Ensure the contacts exist and belong to the same customer
    contact_ids = [contact.id for contact in interaction.contacts]
    existing_contacts = db.query(Contacts).filter(Contacts.id.in_(contact_ids)).all()
    if len(existing_contacts) != len(contact_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more contacts not found",
        )
    for contact in existing_contacts:
        if contact.customer_fk != interaction.customer_fk:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more contacts do not belong to the specified customer",
            )

    new_interaction_dict = interaction.model_dump(exclude={"contacts"})
    new_interaction_sqla = Interactions(**new_interaction_dict)
    db.add(new_interaction_sqla)
    db.commit()

    for contact_id in contact_ids:
        interaction_contacts_sqla = InteractionContacts(
            interactions_fk=new_interaction_sqla.id,
            contacts_fk=contact_id,
        )
        db.add(interaction_contacts_sqla)
    db.flush()
    db.commit()

    return new_interaction_sqla
    # return InteractionResponse.from_interaction(new_interaction)


@router.get("/{interaction_id}")
def get_one_interaction(interaction_id: UUID, db: Session = Depends(get_db)) -> InteractionResponse:
    interaction = db.query(Interactions).filter(Interactions.id == interaction_id).first()
    if not interaction:
        raise EntityDoesNotExistError
    return interaction


@router.put("/{interaction_id}")
def update_interaction(  # noqa: C901, PLR0912
    interaction_id: UUID,
    updated_interaction_pyd: InteractionUpdate,
    db: Session = Depends(get_db),
) -> InteractionResponse:
    interaction = db.query(Interactions).filter(Interactions.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interaction not found")
        # raise custom exception

    update_inter_dict = updated_interaction_pyd.model_dump(exclude_unset=True)

    # Update the customer first
    if "customer_fk" in update_inter_dict:
        customer = (
            db.query(Customers).filter(Customers.id == update_inter_dict["customer_fk"]).first()
        )
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        interaction.customer_fk = update_inter_dict["customer_fk"]

        db.commit()
        db.refresh(interaction)

        # For new customer - validate and update contacts
        contact_ids = [contact.id for contact in updated_interaction_pyd.contacts]
        existing_contacts = db.query(Contacts).filter(Contacts.id.in_(contact_ids)).all()
        if len(existing_contacts) != len(contact_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more contacts not found",
            )

        for contact in existing_contacts:
            if contact.customer_fk != interaction.customer_fk:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more contacts do not belong to the specified customer",
                )

        db.query(InteractionContacts).filter(
            InteractionContacts.interactions_fk == interaction_id,
        ).delete()
        for contact_id in contact_ids:
            interaction_contact = InteractionContacts(
                interactions_fk=interaction.id,
                contacts_fk=contact_id,
            )
            db.add(interaction_contact)
        del update_inter_dict["contacts"]

    # Validate and update contacts when customer hasn't changed
    if "customer_fk" not in update_inter_dict and "contacts" in update_inter_dict:
        contact_ids = [contact.id for contact in updated_interaction_pyd.contacts]
        existing_contacts = db.query(Contacts).filter(Contacts.id.in_(contact_ids)).all()
        if len(existing_contacts) != len(contact_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more contacts not found",
            )

        for contact in existing_contacts:
            if contact.customer_fk != interaction.customer_fk:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more contacts do not belong to the specified customer",
                )

        db.query(InteractionContacts).filter(
            InteractionContacts.interactions_fk == interaction_id,
        ).delete()
        for contact_id in contact_ids:
            interaction_contact = InteractionContacts(
                interactions_fk=interaction.id,
                contacts_fk=contact_id,
            )
            db.add(interaction_contact)
        del update_inter_dict["contacts"]

    # Update other fields
    for key, value in update_inter_dict.items():
        setattr(interaction, key, value)

    db.commit()
    db.refresh(interaction)

    return interaction


@router.delete("/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interaction(interaction_id: UUID, db: Session = Depends(get_db)) -> None:
    interaction = db.query(Interactions).filter(Interactions.id == interaction_id).first()
    if interaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.query(InteractionContacts).filter(
        InteractionContacts.interactions_fk == interaction_id,
    ).delete()
    db.delete(interaction)
    db.commit()
