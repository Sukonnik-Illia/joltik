# from sqlalchemy.orm import Mapped, mapped_column, Enum
# from models.database import CrmBase

# class LeadStatus(CrmBase):
#     __tablename__ = "lead_status"
#     status_name: Mapped[str] = mapped_column(nullable=False)


# def load_json(json_file):
#     with open(json_file, 'r') as file:
#         return (json.load(file))

# def add_statuses(session, statuses_data):
#     statuses = [LeadStatus(**data) for data in statuses_data]
#     session.bulk_save_objects(statuses)
#     session.commit()
