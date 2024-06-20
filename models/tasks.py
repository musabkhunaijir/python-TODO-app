from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
    ForeignKey,
    UniqueConstraint,
)

from configs.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    # __table_args__ = (UniqueConstraint("user_id", "order_id", name="uix_1"),)
