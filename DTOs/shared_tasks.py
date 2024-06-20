from pydantic import BaseModel


class ShareTaskDto(BaseModel):
    task_id: int
    viewer_id: int
