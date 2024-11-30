from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class StudentBase(BaseModel):
    last_name: str = Field(..., max_length=100)
    first_name: str = Field(..., max_length=100)
    middle_name: str = Field(..., max_length=100)
    course: int = Field(..., ge=1, le=6)
    group: str = Field(..., max_length=20)
    faculty: str = Field(..., max_length=100)


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    items: list[Student]
    total: int
    page: int
    size: int
    pages: int
