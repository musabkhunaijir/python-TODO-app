from pydantic import BaseModel


class AddTaskDto(BaseModel):
    title: str
