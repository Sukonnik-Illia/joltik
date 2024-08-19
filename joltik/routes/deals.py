from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.errors import EntityDoesNotExistError
from joltik.models import Contacts, Customers, Deals, Services
from joltik.models.deals import Deal_stage, Deal_type

router = APIRouter()


class DealCreate(BaseModel):
    deal_name: str
    deal_type: Deal_type
    stage: Deal_stage
    ammount: int
    comments: str | None = None
    contact_fk: UUID
    service_fk: UUID
    customer_fk: UUID

    class Config:
        from_attributes = True


class DealUpdate(BaseModel):
    deal_name: str | None = None
    deal_type: Deal_type | None = None
    stage: Deal_stage | None = None
    ammount: int | None = None
    comments: str | None = None
    contact_fk: UUID | None = None
    service_fk: UUID | None = None
    customer_fk: UUID | None = None

    class Config:
        from_attributes = True


class DealResponse(DealCreate):
    id: UUID

    class Config:
        from_attributes = True


@router.get("/")
def list_deals(db: Session = Depends(get_db)) -> List[DealResponse]:
    return db.query(Deals).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_deal(deal: DealCreate, db: Session = Depends(get_db)) -> DealResponse:
    customer = db.query(Customers).filter(Customers.id == deal.customer_fk).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    contact = db.query(Contacts).filter(Contacts.id == deal.contact_fk).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if contact.customer_fk != deal.customer_fk:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more contacts do not belong to the specified customer",
        )
    service = db.query(Services).filter(Services.id == deal.service_fk).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    new_deal_dict = deal.model_dump(mode="json")
    new_deal_sqla = Deals(**new_deal_dict)
    db.add(new_deal_sqla)
    db.commit()
    return new_deal_sqla


@router.get("/{deal_id}")
def get_one_deal(deal_id: UUID, db: Session = Depends(get_db)) -> DealResponse:
    deal = db.query(Deals).filter(Deals.id == deal_id).first()
    if not deal:
        raise EntityDoesNotExistError
    return deal


@router.put("/{deal_id}")
def update_deal(  # noqa: C901
    deal_id: UUID,
    updated_deal_pyd: DealUpdate,
    db: Session = Depends(get_db),
) -> DealResponse:
    deal_sqla = db.query(Deals).filter(Deals.id == deal_id).first()
    if not deal_sqla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    updated_deal_dict = updated_deal_pyd.model_dump(mode="json", exclude_unset=True)

    if "service_fk" in updated_deal_dict:
        service = db.query(Services).filter(Services.id == updated_deal_dict["service_fk"]).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    if "customer_fk" in updated_deal_dict:
        customer = (
            db.query(Customers).filter(Customers.id == updated_deal_dict["customer_fk"]).first()
        )
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        if "contact_fk" not in updated_deal_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact update required when change customer",
            )

    if "contact_fk" in updated_deal_dict:
        contact = db.query(Contacts).filter(Contacts.id == updated_deal_dict["contact_fk"]).first()
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

        if (
            "customer_fk" in updated_deal_dict
            and contact.customer_fk != updated_deal_pyd.customer_fk
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer does not have the specified contact",
            )

        if "customer_fk" not in updated_deal_dict and contact.customer_fk != deal_sqla.customer_fk:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contact does not belong to the specified customer",
            )

    for key, value in updated_deal_dict.items():
        setattr(deal_sqla, key, value)

    db.commit()
    db.refresh(deal_sqla)
    return deal_sqla


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(deal_id: UUID, db: Session = Depends(get_db)) -> None:
    deal = db.query(Deals).filter(Deals.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    db.delete(deal)
    db.commit()
