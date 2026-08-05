from pydantic import BaseModel, EmailStr
from udemy_course.db.models import STATUS_CHOICES, TYPE_CHOICES
from typing import Optional
from datetime import datetime


class UserProfileRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: str | None
    age: Optional[int] = None
    profile_picture: str | None
    password: str

    class Config:
        from_attributes = True

class UserProfileLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True

class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: str | None
    age: Optional[int] = None
    profile_picture: str | None
    created_date: datetime

    class Config:
        from_attributes = True


class CategoryCreateSchema(BaseModel):
    category_name: str

    class Config:
        from_attributes = True

class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class CourseCreateSchema(BaseModel):
    course_name: str
    description: str
    level: STATUS_CHOICES
    price: float
    type_course: TYPE_CHOICES
    course_certificate: bool
    category_id: int
    author_id: int

    class Config:
        from_attributes = True

class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
    level: STATUS_CHOICES
    price: float
    type_course: TYPE_CHOICES
    course_certificate: bool
    created_date: datetime
    category_id: int
    author_id: int

    class Config:
        from_attributes = True


class LessonCreateSchema(BaseModel):
    title: str
    video_url: Optional[str] = None
    video: str | None
    content: str
    course_id: int

    class Config:
        from_attributes = True

class LessonSchema(BaseModel):
    id: int
    title: str
    video_url: Optional[str] = None
    video: str | None
    content: str
    course_id: int

    class Config:
        from_attributes = True


class ReviewCreateSchema(BaseModel):
    text: str | None
    stars: Optional[int]
    course_id: int
    user_id: int

    class Config:
        from_attributes = True

class ReviewSchema(BaseModel):
    id: int
    text: str | None
    stars: Optional[int]
    created_date: datetime
    course_id: int
    user_id: int

    class Config:
        from_attributes = True
