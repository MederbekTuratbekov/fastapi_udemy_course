from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .database import Base
from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import String, Integer, Enum, DECIMAL, Text, Boolean, TIMESTAMP, ForeignKey


class UserProfile(Base):
    __tablename__ = 'userprofile'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    profile_picture: Mapped[str | None] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))

    course_author: Mapped[List['Course']] = relationship('Course', back_populates='author', cascade='all, delete-orphan')
    review_user: Mapped[List['Review']] = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    refresh_token_user: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')

    def __str__(self):
        return f'{UserProfile.username}'

class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=lambda:datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='refresh_token_user')

    def __str__(self):
        return f'{RefreshToken.token}'

class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(30), unique=True)

    course_category: Mapped[List['Course']] = relationship('Course', back_populates='category', cascade='all, delete-orphan')

    def __str__(self):
        return f'{Category.category_name}'


class STATUS_CHOICES(str, PyEnum):
    easy = 'easy'
    simple = 'simple'
    hard = 'hard'

class TYPE_CHOICES(str, PyEnum):
    free = 'free'
    paid = 'paid'


class Course(Base):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    course_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    level: Mapped[STATUS_CHOICES] = mapped_column(Enum(STATUS_CHOICES), default=STATUS_CHOICES.simple)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    type_course: Mapped[TYPE_CHOICES] = mapped_column(Enum(TYPE_CHOICES), default=TYPE_CHOICES.paid)
    course_certificate: Mapped[bool] = mapped_column(Boolean, default=True)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship('Category', back_populates='course_category')
    author_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    author: Mapped['UserProfile'] = relationship('UserProfile', back_populates='course_author')

    lesson_course: Mapped[List['Lesson']] = relationship('Lesson', back_populates='course', cascade='all, delete-orphan')
    review_course: Mapped[List['Review']] = relationship('Review', back_populates='course', cascade='all, delete-orphan')

    def __str__(self):
        return f'{Course.type_course}'


class Lesson(Base):
    __tablename__ = 'lesson'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped['Course'] = relationship('Course', back_populates='lesson_course')

    def __str__(self):
        return f'{Lesson.title}'


class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=lambda : datetime.now(timezone.utc))
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped['Course'] = relationship('Course', back_populates='review_course')
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='review_user')

    def __str__(self):
        return f'{Review.text}'
