from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.models import Services
from joltik.models.services import Service as ServiceType

router = APIRouter()


class ServiceCreate(BaseModel):
    service_type: ServiceType
    description: str

    class Config:
        from_attributes = True


class ServiceResponse(ServiceCreate):
    id: UUID


@router.get("/")
def list_all(db: Session = Depends(get_db)) -> list[ServiceResponse]:
    return db.query(Services).all()
    # resp=[]
    # for service in db.query(Services).all():
    #     resp.append(
    #         ServiceResponce(service_type = service.service_type, description=service.description)
    #     )
    # return resp


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_service(req_service: ServiceCreate, db: Session = Depends(get_db)) -> ServiceResponse:
    service = Services(**jsonable_encoder(req_service))
    db.add(service)
    db.commit()
    return service


@router.get("/{service_id}", response_model=ServiceResponse)
def list_one(service_id: UUID, db: Session = Depends(get_db)) -> ServiceResponse:
    service = db.query(Services).filter(Services.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return service


@router.put("/{service_id}", status_code=status.HTTP_202_ACCEPTED)
def update_service(
    service_id: UUID,
    service_update: ServiceCreate,
    db: Session = Depends(get_db),
) -> ServiceResponse:
    service = db.query(Services).filter(Services.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    service.service_type = service_update.service_type  # ENUM, need check for Unprocessable Entity
    service.description = service_update.description
    db.commit()
    db.refresh(service)
    return service
