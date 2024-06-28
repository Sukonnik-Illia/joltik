from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from joltik.db import get_db
from joltik.models import Services
from joltik.models.services import Service as ServiceType

app = FastAPI()


class ServiceResponce(BaseModel):
    service_type: ServiceType
    description: str

    class Config:
        orm_mode = True


@app.get("/")
def first(db: Session = Depends(get_db)) -> list[ServiceResponce]:
    return db.query(Services).all()
    # resp=[]
    # for service in db.query(Services).all():
    #     resp.append(
    #         ServiceResponce(service_type = service.service_type, description=service.description)
    #     )
    # return resp
