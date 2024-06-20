from pydantic import BaseModel


class AddTaskDto(BaseModel):
    title: str


class ModifyDto(BaseModel):
    task_id: int
    title: str


class DeleteTaskDto(BaseModel):
    user_id: int
