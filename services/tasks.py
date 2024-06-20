from sqlalchemy import and_, update
from fastapi import HTTPException
from sqlalchemy.orm import Session


from models.users import UserModel
from models.tasks import TaskModel
from DTOs.tasks import AddTaskDto, ModifyDto, DeleteTaskDto


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

    def add(self, add_task_dto: AddTaskDto):
        # 1- check if user is already registered
        is_user = self.__getCurrentUserById()

        if not bool(is_user):
            raise HTTPException(status_code=404, detail="user not found")

        # 2- get last task order id to be incremented
        last_task = self.__getLastTaskById()
        current_order_id = last_task.order_id + 1 if last_task else 1

        db_task = TaskModel(
            title=add_task_dto.title, user_id=self.user_id, order_id=current_order_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return "created"

    def modify(self, modify_task_Dto: ModifyDto):
        # 1- check that task does exist
        is_task = self.getOneUserTask(modify_task_Dto.task_id)

        if not bool(is_task):
            raise HTTPException(status_code=404, detail="task not found")

        # update the record
        self.db.query(TaskModel).filter(
            and_(
                TaskModel.id == modify_task_Dto.task_id,
                TaskModel.user_id == self.user_id,
            )
        ).update({TaskModel.title: modify_task_Dto.title})
        self.db.commit()

        return "updated"

    def delete(self, task_id: int, delete_task_Dto: DeleteTaskDto):
        # 1- check that task does exist
        is_task = self.getOneUserTask(task_id)

        if not bool(is_task):
            raise HTTPException(status_code=404, detail="task not found")

            # update the record
        self.db.query(TaskModel).filter(
            and_(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id,
            )
        ).delete()
        self.db.commit()

        return "deleted"

    def getOneUserTask(self, task_id):
        return (
            self.db.query(TaskModel)
            .filter(
                and_(
                    TaskModel.id == task_id,
                    TaskModel.user_id == self.user_id,
                )
            )
            .first()
        )

    # TODO:(refactor) should be in user's domain service
    def __getCurrentUserById(self):
        return (
            self.db.query(UserModel)
            .filter(
                UserModel.id == self.user_id,
            )
            .first()
        )

    def __getLastTaskById(self):
        return (
            self.db.query(TaskModel)
            .filter(
                TaskModel.user_id == self.user_id,
            )
            .order_by(TaskModel.order_id.desc())
            .first()
        )
