from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI

from configs.database import Base, engine, get_db

# USERS
from services.users import UsersService
from DTOs.users import RegisterUserDto, LoginUserDto

# TASKS
from services.tasks import TasksService
from DTOs.shared_tasks import ShareTaskDto
from DTOs.tasks import AddTaskDto, ModifyDto, UserIdDto, ReorderTasksDto

# SHARED TASKS
from services.shared_tasks import SharedTasksService


# DB migration
import models.users
import models.tasks
import models.shared_tasks

Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()


# ** users APIs **
@app.post("/v1/users/register")
def register(user_dto: RegisterUserDto, db: Session = Depends(get_db)):
    return UsersService().register(user_dto, db=db)


@app.post("/v1/users/login")
def register(login_dto: LoginUserDto, db: Session = Depends(get_db)):
    return UsersService().login(login_dto, db=db)


# ** tasks APIs **
@app.post("/v1/tasks/{user_id}")
def register(user_id, add_task_dto: AddTaskDto, db: Session = Depends(get_db)):
    return TasksService(db, user_id).add(
        add_task_dto,
    )


@app.get("/v1/tasks/{user_id}")
def getCurrentUserTasks(user_id, db: Session = Depends(get_db)):
    return TasksService(db, user_id).getCurrentUserTasks()


@app.patch("/v1/tasks/user/{user_id}")
def modify(user_id, modify_task_dto: ModifyDto, db: Session = Depends(get_db)):
    return TasksService(db, user_id).modify(modify_task_dto)


@app.delete("/v1/tasks/{task_id}")
def deleteTask(task_id, delete_task_dto: UserIdDto, db: Session = Depends(get_db)):
    return TasksService(db, delete_task_dto.user_id).delete(task_id)


@app.patch("/v1/tasks/reorder")
def modify(reorder_task_dto: ReorderTasksDto, db: Session = Depends(get_db)):
    return TasksService(db, reorder_task_dto.user_id).reorder(reorder_task_dto)


@app.patch("/v1/tasks/{task_id}/mark-done")
def markTaskDone(task_id, mark_done_dto: UserIdDto, db: Session = Depends(get_db)):
    return TasksService(db, mark_done_dto.user_id).markDone(task_id)


# ** shared tasks APIs **


@app.get("/v1/shared-tasks/{viewer_id}")
def getSharedTasks(viewer_id, db: Session = Depends(get_db)):
    return SharedTasksService(db, viewer_id).getSharedTasks()


@app.post("/v1/shared-tasks/{user_id}/share")
def markTaskDone(user_id, share_task_dto: ShareTaskDto, db: Session = Depends(get_db)):
    return SharedTasksService(db, user_id).share(share_task_dto)
