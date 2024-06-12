from sqlalchemy.orm import Mapped, as_declarative, mapped_column


@as_declarative()
class CrmBase:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
