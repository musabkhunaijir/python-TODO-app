from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped

from configs.database import Base


class SharedTasksModel(Base):
    __tablename__ = "shared_tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    viewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    __table_args__ = (UniqueConstraint("viewer_id", "task_id", name="uix_1"),)

    viewer: Mapped["UserModel"] = relationship(back_populates="shared_tasks")
    task: Mapped["TaskModel"] = relationship(
        back_populates="shared_tasks",
    )
