from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from joltik.models.database import CrmBase

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

with Session(engine) as session:
    CrmBase.metadata.create_all(engine)
