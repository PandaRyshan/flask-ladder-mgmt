import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from src.dto.role_dto import RoleDTO
from src.contants import RoleEnum


class UserDTO(BaseModel):
    """
    Data Transfer Object (DTO) for representing a user.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        email (Optional[EmailStr]): The email address of the user (optional).
        name (str): The name of the user.
        is_active (Optional[bool]): Indicates if the user is active (optional, default is False).
        is_verified (Optional[bool]): Indicates if the user is verified (optional, default is False).
        roles (Optional[list[RoleDto]]): The roles assigned to the user (optional, default is [RoleDto(id=RoleEnum.USER.value, name=RoleEnum.USER.name)]).
        fs_uniquifier (str): The filesystem uniquifier of the user.
        created_at (Optional[datetime]): The timestamp when the user was created (optional, default is the current datetime).
        updated_at (Optional[datetime]): The timestamp when the user was last updated (optional, default is the current datetime).
    """
    id: Optional[int] = None
    email: EmailStr
    username: Optional[str] = None
    password: str
    name: str
    active: str = True
    # is_active: Optional[bool] = False
    # is_verified: Optional[bool] = False
    # is_authenticated: Optional[bool] = False
    # is_anonymous: Optional[bool] = True
    roles: Optional[list[RoleDTO]] = [RoleDTO(
        id=RoleEnum.USER.value, name=RoleEnum.USER.name)]
    fs_uniquifier: Optional[str] = uuid.uuid4().hex
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    current_login_at: Optional[datetime] = None
    login_count: Optional[int] = 0
