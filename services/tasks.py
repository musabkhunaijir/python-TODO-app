from fastapi import HTTPException
from sqlalchemy.orm import Session


from DTOs.tasks import AddTaskDto
from models.users import UserModel
from models.tasks import TaskModel


class TasksService:
    def __init__(self, db: Session, user_id):
        self.db = db
        self.user_id = user_id

    def getCurrentUserTasks(self):
        # TODO: add pagination
        return (
            self.db.query(TaskModel)
            .filter(
                UserModel.id == self.user_id,
            )
            .order_by(TaskModel.order_id.asc())
            .all()
        )

    def addTask(self, add_task_dto: AddTaskDto):
        # 1- check if user is already registered
        is_user = self.getCurrentUserById()

        if not bool(is_user):
            raise HTTPException(status_code=404, detail="user not found")

        # 2- get last task order id to be incremented
        last_task = self.getLastTaskById()
        current_order_id = last_task.order_id + 1 if last_task else 1

        print(current_order_id)
        # return

        db_task = TaskModel(
            title=add_task_dto.title, user_id=self.user_id, order_id=current_order_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return "created"

    # TODO:(refactor) should be in user's domain service
    def getCurrentUserById(self):
        return (
            self.db.query(UserModel)
            .filter(
                UserModel.id == self.user_id,
            )
            .first()
        )

    def getLastTaskById(self):
        return (
            self.db.query(TaskModel)
            .filter(
                UserModel.id == self.user_id,
            )
            .order_by(TaskModel.order_id.desc())
            .first()
        )
