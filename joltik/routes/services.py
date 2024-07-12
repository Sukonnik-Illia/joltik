from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select

from joltik.auth.user_manager import current_active_user
from joltik.db import DBAsyncSession
from joltik.models import Services
from joltik.models.services import Service as ServiceType
from joltik.models.users import User

router = APIRouter()


class ServiceCreate(BaseModel):
    service_type: ServiceType
    description: str

    class Config:
        from_attributes = True


class ServiceResponse(ServiceCreate):
    id: UUID


@router.get("/")
async def list_all_services(
    db: DBAsyncSession,
    _: User = Depends(current_active_user),
) -> list[ServiceResponse]:
    result = await db.execute(select(Services))
    return result.scalars().all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(service_pyd: ServiceCreate, db: DBAsyncSession) -> ServiceResponse:
    new_service_sqla = Services(**jsonable_encoder(service_pyd))
    db.add(new_service_sqla)
    await db.commit()
    await db.refresh(new_service_sqla)
    return new_service_sqla


@router.get("/{service_id}", response_model=ServiceResponse)
async def select_service(service_id: UUID, db: DBAsyncSession) -> ServiceResponse:
    service = await db.get(Services, service_id)
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return service


@router.put("/{service_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_service(
    service_id: UUID,
    updated_service_pyd: ServiceCreate,
    db: DBAsyncSession,
) -> ServiceResponse:
    service_sqla = await db.get(Services, service_id)
    if not service_sqla:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_service_dict = updated_service_pyd.model_dump(exclude_unset=True)
    for key, value in update_service_dict.items():
        setattr(service_sqla, key, value)
    await db.commit()
    await db.refresh(service_sqla)
    return service_sqla


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: UUID, db: DBAsyncSession) -> None:
    service_sqla = await db.get(Services, service_id)
    if service_sqla is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(service_sqla)
    await db.commit()
