from typing import Type

from pydantic import BaseModel, EmailStr, ValidationError, validator

from crud import get_items
from error import HttpError
from models import User, get_session_maker

Session = get_session_maker()


class CreateAds(BaseModel):
    title: str
    description: str
    autor: int | str

    @validator("autor")
    def autorit(cls, values):
        with Session() as session:
            item = get_items(session, User, values)
            if item is None:
                raise HttpError(404, "user not found")
            return values


class UpdateAds(BaseModel):
    title: str
    description: str


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("password")
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is to short")
        return value


def validate(validation_schema: Type[CreateAds] | Type[CreateUser], json_data):
    try:
        validated = validation_schema(**json_data).dict(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated
