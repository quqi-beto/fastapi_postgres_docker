from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# User Schemas
class UserBase(BaseModel):
    """Base schema for User with common fields."""

    username: str
    email: str


class UserCreate(UserBase):
    """Schema for creating a new User."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating a User."""

    username: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    """Schema for User response."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Todo Schemas
class TodoBase(BaseModel):
    """Base schema for Todo with common fields."""

    title: str
    description: Optional[str] = None
    user_id: int


class TodoCreate(TodoBase):
    """Schema for creating a new Todo."""

    pass


class TodoUpdate(BaseModel):
    """Schema for updating a Todo."""

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    """Schema for Todo response."""

    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    date_completed: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
