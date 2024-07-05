# from typing import List, Union
# from uuid import UUID, uuid4

# from fastapi import APIRouter, Depends, HTTPException, status
# from pydantic import BaseModel
# from sqlalchemy.orm import Session

# from joltik.db import get_db
# from joltik.models import Contacts, Customers, Deals, Services
# from joltik.models.deals import Deal_type, Deal_stage

# router = APIRouter()


# class DealCreate(BaseModel):
#     deal_name: str
#     deal_type = Deal_type
#     stage = Deal_stage
#     ammount: int
#     comments: str | None = None
#     contact_fk: UUID
#     service_fk: UUID
#     customer_fk: UUID

#     class Config:
#         from_attributes = True


# class DealUpdate(BaseModel):
#     deal_name: str | None = None
#     deal_type: Deal_type | None = None
#     stage: Deal_stage | None = None
#     ammount: int | None = None
#     comments: str | None = None
#     contact_fk: UUID | None = None
#     service_fk: UUID | None = None
#     customer_fk: UUID | None = None

#     class Config:
#         from_attributes = True


# class DealResponse(DealCreate):
#     id: UUID

#     class Config:
#         from_attributes = True


# @router.get("/")
# def list_deals(db: Session = Depends(get_db)) -> List[DealResponse]:
#     return db.query(Deals).all()


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_deal(deal: DealCreate, db: Session = Depends(get_db)) -> DealResponse:
#     customer = db.query(Customers).filter(Customers.id == deal.customer_fk).first()
#     if not customer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
#     contact = db.query(Contacts).filter(Contacts.id == deal.contact_fk).first()
#     if not contact:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     if contact.customer_fk != deal.customer_fk:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="One or more contacts do not belong to the specified customer",
#         )
#     service = db.query(Services).filter(Services.id == deal.service_fk).first()
#     if not service:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

#     new_deal_dict = deal.model_dump(mode="json")
#     new_deal_sqla = Deals(**new_deal_dict)
#     db.add(new_deal_sqla)
#     db.commit()
#     return new_deal_sqla
