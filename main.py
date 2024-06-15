from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI

from configs.database import Base, engine, get_db

# USERS
from services.users import UsersService
from DTOs.users import RegisterUserDto, LoginUserDto

# TASKS
from DTOs.tasks import AddTaskDto, ModifyDto
from services.tasks import TasksService

# from models.users import UserModel
# from models.tasks import TaskModel


# DB migration
import models.users
import models.tasks

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
def modify(user_id, modify_task_Dto: ModifyDto, db: Session = Depends(get_db)):
    return TasksService(db, user_id).modify(modify_task_Dto)
