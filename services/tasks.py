from sqlalchemy import or_, and_
from fastapi import HTTPException
from sqlalchemy.orm import Session


from models.users import UserModel
from models.tasks import TaskModel
from DTOs.tasks import AddTaskDto


class TasksService:
    def __init__(self, user_id):
        self.user_id = user_id

    def addTask(self, add_task_dto: AddTaskDto, db: Session):
        # 1- check if user is already registered
        is_user = (
            db.query(UserModel)
            .filter(
                UserModel.id == self.user_id,
            )
            .first()
        )

        if not bool(is_user):
            raise HTTPException(status_code=404, detail="user not found")

        db_task = TaskModel(
            title=add_task_dto.title,
            user_id=self.user_id,
            order_id=add_task_dto.order_id,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return "created"
