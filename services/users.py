from sqlalchemy import or_, and_
from fastapi import HTTPException
from sqlalchemy.orm import Session


from models.users import UserModel
from utils.passwords import hashPassword, verifyPassword
from DTOs.users import RegisterUserDto, LoginUserDto


class UsersService:
    def register(self, register_dto: RegisterUserDto, db: Session):
        # 1- check if user is already registered
        is_user = (
            db.query(UserModel)
            .filter(
                or_(
                    UserModel.email == register_dto.email,
                    UserModel.username == register_dto.username,
                )
            )
            .first()
        )

        if bool(is_user):
            raise HTTPException(status_code=400, detail="user already exist")

        # 2- create user if it's new
        hashed_pass = hashPassword(register_dto.password)

        db_user = UserModel(
            username=register_dto.username,
            email=register_dto.email,
            password=hashed_pass,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return "created"

    def login(self, login_dto: LoginUserDto, db: Session):
        is_user = (
            db.query(UserModel)
            .filter(
                and_(
                    UserModel.username == login_dto.username,
                )
            )
            .first()
        )

        isVerified = verifyPassword(
            plain_password=login_dto.password, stored_password=is_user.password
        )

        if not bool(isVerified):
            raise HTTPException(status_code=400, detail="invalid credentials")

        return "some-token"
