import datetime

from sqlalchemy import String, Float, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Operation(Base):
    __tablename__ = "operations"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    expression: Mapped[str] = mapped_column(String(256), nullable=False)
    result = mapped_column(Float, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'expression', name='uix_user_expression'),
    )
