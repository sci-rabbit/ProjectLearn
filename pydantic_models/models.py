import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    surname: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("name")
    def validator_name(cls, value):
        if not re.match(r"^[a-zA-Zа-яА-Я'-]+$", value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )

        return value

    @field_validator("surname")
    def validator_surname(cls, value):
        if not re.match(r"^[a-zA-Zа-яА-Я'-]+$", value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )

        return value


class ShowUser(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    password: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=20)
    surname: Optional[str] = Field(default=None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=64)
    is_active: Optional[bool] = None

    @field_validator("name")
    def validator_name(cls, value):
        if value is not None:
            if not re.match(r"^[a-zA-Zа-яА-Я'-]+$", value):
                raise HTTPException(
                    status_code=422, detail="Name should contains only letters"
                )

            return value

    @field_validator("surname")
    def validator_surname(cls, value):
        if value is not None:
            if not re.match(r"^[a-zA-Zа-яА-Я'-]+$", value):
                raise HTTPException(
                    status_code=422, detail="Name should contains only letters"
                )

            return value


class UpdateUserResponse(BaseModel):
    id: uuid.UUID


class DeleteUserResponse(BaseModel):
    id: uuid.UUID
