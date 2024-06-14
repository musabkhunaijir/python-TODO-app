from pydantic import BaseModel

class RegisterUserDto(BaseModel):
    username:str
    email:str
    password:str


class LoginUserDto(BaseModel):
    username:str
    password:str