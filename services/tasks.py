from sqlalchemy import and_
from fastapi import HTTPException
from sqlalchemy.orm import Session


from models.users import UserModel
from models.tasks import TaskModel, StatusEnum
from DTOs.tasks import AddTaskDto, ModifyDto, ReorderTasksDto


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

    def modify(self, modify_task_dto: ModifyDto):
        # 1- check that task does exist
        is_task = self.getOneUserTask(modify_task_dto.task_id)

        if not bool(is_task):
            raise HTTPException(status_code=404, detail="task not found")

        # update the record
        self.db.query(TaskModel).filter(
            and_(
                TaskModel.id == modify_task_dto.task_id,
                TaskModel.user_id == self.user_id,
            )
        ).update({TaskModel.title: modify_task_dto.title})
        self.db.commit()

        return "updated"

    def delete(self, task_id: int):
        # 1- check that task does exist
        is_task = self.getOneUserTask(task_id)

        if not bool(is_task):
            raise HTTPException(status_code=404, detail="task not found")

        # delete the record
        self.db.query(TaskModel).filter(
            and_(
                TaskModel.id == task_id,
                TaskModel.user_id == self.user_id,
            )
        ).delete()
        self.db.commit()

        return "deleted"

    def reorder(self, reorder_task_dto: ReorderTasksDto):
        # 1- check that all task does exist
        for task in reorder_task_dto.tasks:
            is_task = self.getOneUserTask(task.id)
            if not is_task:
                raise HTTPException(
                    status_code=404, detail=f"task {task.id}, not found"
                )

        # 2- update each task order_id
        for task in reorder_task_dto.tasks:
            # update the record
            self.updateTaskOrder(task)

        return "tasks reorder"

    def markDone(self, task_id: int):
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
        ).update({TaskModel.status: StatusEnum.done})
        self.db.commit()

        return "status updated"

    def updateTaskOrder(self, task):
        self.db.query(TaskModel).filter(
            and_(
                TaskModel.id == task.id,
                TaskModel.user_id == self.user_id,
            )
        ).update({TaskModel.order_id: task.order_id})
        self.db.commit()

    def getOneUserTask(self, task_id):
        return (
            self.db.query(TaskModel)
            .filter(
                and_(
                    TaskModel.id == task_id,
                    TaskModel.user_id == self.user_id,
                    TaskModel.status == StatusEnum.todo,
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
