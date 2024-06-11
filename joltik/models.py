# import sqlalchemy
# print("Версия SQLAlchemy:", sqlalchemy.__version__)

from sqlalchemy import ForeignKey, create_engine, select
from sqlalchemy.orm import Mapped, Session, as_declarative, mapped_column

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class CustomerModel(AbstractModel):
    __tablename__ = "customers"
    company_name: Mapped[int] = mapped_column()
    industry: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()


class PersonModel(AbstractModel):
    __tablename__ = "contact_persons"
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    job_title: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[int] = mapped_column()
    comment: Mapped[str] = mapped_column()


# print(CustomerModel.__table__.__dict__)
# print(PersonModel.__table__.__dict__)

with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        customer = CustomerModel(
            id=1,
            company_name="Romashka",
            industry="flowers",
            address="FarFarAway",
        )
        session.add(customer)
    with session.begin():
        res = session.execute(select(CustomerModel).where(CustomerModel.id == 1))
        # print(res.scalar())

# customers_table = Table(
#     "customers",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("company_name", String(50), nullable=False),
#     Column("industry", String(50)),
#     Column("address", String(255))
# )

# contacts_table = Table(
#     "contact_persons",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("customer_id", ForeignKey('customers.id')),
#     Column("first_name",String(50), nullable=False),
#     Column("last_name",String(50), nullable=False),
#     Column("job_title",String(50), nullable=False),
#     Column("email",String(100), nullable=False),
#     Column("phone_number",String(15)),
#     Column("comment",Text)
# )

# metadata.create_all(engine)
# metadata.drop_all(engine)
