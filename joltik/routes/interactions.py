from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from joltik.db import DBAsyncSession
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
async def list_all_interactions(db: DBAsyncSession) -> List[InteractionResponse]:
    result = await db.execute(
        select(Interactions).options(
            selectinload(Interactions.customer),
            selectinload(Interactions.contacts),
        ),
    )
    return result.scalars().all()
    # return [InteractionResponse.model_validate(interaction) for interaction in interactions]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_interaction(
    interaction: InteractionCreate,
    db: DBAsyncSession,
) -> InteractionResponse:
    # Ensure the customer exists
    customer = await db.execute(select(Customers).filter(Customers.id == interaction.customer_fk))
    customer = customer.scalars().first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Ensure the contacts exist and belong to the same customer
    contact_ids = [contact.id for contact in interaction.contacts]
    existing_contacts = await db.execute(
        select(Contacts)
        .options(selectinload(Contacts.customer))
        .filter(Contacts.id.in_(contact_ids)),
    )
    existing_contacts = existing_contacts.scalars().all()
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

    new_interaction_dict = interaction.model_dump(mode="json", exclude={"contacts"})
    new_interaction_sqla = Interactions(**new_interaction_dict)
    db.add(new_interaction_sqla)
    await db.commit()

    for contact_id in contact_ids:
        interaction_contacts_sqla = InteractionContacts(
            interactions_fk=new_interaction_sqla.id,
            contacts_fk=contact_id,
        )
        db.add(interaction_contacts_sqla)
    await db.commit()
    await new_interaction_sqla.awaitable_attrs.contacts

    return new_interaction_sqla
    # return InteractionResponse.from_interaction(new_interaction)


@router.get("/{interaction_id}")
async def select_interaction(interaction_id: UUID, db: DBAsyncSession) -> InteractionResponse:
    result = await db.execute(
        select(Interactions)
        .options(selectinload(Interactions.customer), selectinload(Interactions.contacts))
        .filter(Interactions.id == interaction_id),
    )
    interaction = result.scalars().first()
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found",
        )
    return interaction


@router.put("/{interaction_id}")
async def update_interaction(  # noqa: C901, PLR0912
    interaction_id: UUID,
    updated_interaction_pyd: InteractionUpdate,
    db: DBAsyncSession,
) -> InteractionResponse:
    result = await db.execute(
        select(Interactions)
        .options(selectinload(Interactions.customer), selectinload(Interactions.contacts))
        .filter(Interactions.id == interaction_id),
    )
    interaction = result.scalars().first()
    if not interaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interaction not found")

    updated_inter_dict = updated_interaction_pyd.model_dump(mode="json", exclude_unset=True)

    # Update the customer first
    if "customer_fk" in updated_inter_dict:
        customer = await db.execute(
            select(Customers).filter(Customers.id == updated_inter_dict["customer_fk"]),
        )
        customer = customer.scalars().first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        interaction.customer_fk = updated_inter_dict["customer_fk"]

        await db.commit()
        await db.refresh(interaction)

        # For new customer - validate and update contacts
        contact_ids = [contact.id for contact in updated_interaction_pyd.contacts]
        existing_contacts = await db.execute(
            select(Contacts)
            .options(selectinload(Contacts.customer))
            .filter(Contacts.id.in_(contact_ids)),
        )
        existing_contacts = existing_contacts.scalars().all()
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

        await db.execute(
            delete(InteractionContacts).where(
                InteractionContacts.interactions_fk == interaction_id,
            ),
        )
        for contact_id in contact_ids:
            interaction_contact = InteractionContacts(
                interactions_fk=interaction.id,
                contacts_fk=contact_id,
            )
            db.add(interaction_contact)
        del updated_inter_dict["contacts"]

    # Validate and update contacts when customer hasn't changed
    if "customer_fk" not in updated_inter_dict and "contacts" in updated_inter_dict:
        contact_ids = [contact.id for contact in updated_interaction_pyd.contacts]
        existing_contacts = await db.execute(
            select(Contacts)
            .options(selectinload(Contacts.customer))
            .filter(Contacts.id.in_(contact_ids)),
        )
        existing_contacts = existing_contacts.scalars().all()
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

        await db.execute(
            delete(InteractionContacts).where(
                InteractionContacts.interactions_fk == interaction_id,
            ),
        )
        for contact_id in contact_ids:
            interaction_contact = InteractionContacts(
                interactions_fk=interaction.id,
                contacts_fk=contact_id,
            )
            db.add(interaction_contact)
        del updated_inter_dict["contacts"]

    # Update other fields
    for key, value in updated_inter_dict.items():
        setattr(interaction, key, value)

    await db.commit()
    await db.refresh(interaction)

    return interaction


@router.delete("/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interaction(interaction_id: UUID, db: DBAsyncSession) -> None:
    interaction = await db.get(Interactions, interaction_id)
    if interaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.execute(
        delete(InteractionContacts).where(
            InteractionContacts.interactions_fk == interaction_id,
        ),
    )
    await db.delete(interaction)
    await db.commit()
