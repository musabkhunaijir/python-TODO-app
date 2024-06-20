import enum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
    ForeignKey,
    UniqueConstraint,
    Enum,
)

from configs.database import Base


class StatusEnum(enum.Enum):
    todo = "TODO"
    done = "DONE"


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, nullable=False, default=1)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.todo)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    owner: Mapped["UserModel"] = relationship(
        back_populates="tasks",
    )

    shared_tasks: Mapped[list["SharedTasksModel"]] = relationship(
        back_populates="task",
    )

    # __table_args__ = (UniqueConstraint("user_id", "order_id", name="uix_1"),)
