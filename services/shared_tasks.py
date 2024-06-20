from sqlalchemy.orm import Session, joinedload


from models.users import UserModel
from models.tasks import TaskModel
from models.shared_tasks import SharedTasksModel
from DTOs.shared_tasks import ShareTaskDto


class SharedTasksService:
    def __init__(self, db: Session, user_id):
        self.db = db
        self.user_id = user_id

    def getSharedTasks(self):
        return (
            self.db.query(SharedTasksModel)
            .filter(
                SharedTasksModel.viewer_id == self.user_id,
            )
            .options(
                joinedload(
                    SharedTasksModel.viewer,
                    innerjoin=True,
                ).load_only(UserModel.id, UserModel.username)
            )
            .options(
                joinedload(
                    SharedTasksModel.task,
                    innerjoin=True,
                ).options(
                    joinedload(
                        TaskModel.owner,
                        innerjoin=True,
                    ).load_only(UserModel.id, UserModel.username)
                )
            )
            .all()
        )

    def share(self, share_task_dto: ShareTaskDto):
        # 1- TODO: check that user does exist
        # 2- TODO: check that task does exist

        db_shared_task = SharedTasksModel(
            task_id=share_task_dto.task_id,
            viewer_id=share_task_dto.viewer_id,
        )
        self.db.add(db_shared_task)
        self.db.commit()
        self.db.refresh(db_shared_task)

        return "shared"
