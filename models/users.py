from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


from configs.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    shared_tasks: Mapped[list["SharedTasksModel"]] = relationship(
        back_populates="viewer",
    )

    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="owner",
    )
