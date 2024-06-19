import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, as_declarative, mapped_column


@as_declarative()
class CrmBase:
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
