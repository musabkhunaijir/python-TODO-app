from pydantic import BaseModel


class AddTaskDto(BaseModel):
    title: str


class ModifyDto(BaseModel):
    task_id: int
    title: str


class DeleteTaskDto(BaseModel):
    user_id: int


class TaskOrder(BaseModel):
    id: int
    order_id: int


class ReorderTasksDto(BaseModel):
    user_id: int
    tasks: list[TaskOrder]
