from .views import UserProfileAdmin, CategoryAdmin, CourseAdmin, LessonAdmin, ReviewAdmin
from fastapi import FastAPI
from sqladmin import Admin
from udemy_course.db.database import engine


def setup_admin(udemy: FastAPI):
    admin = Admin(udemy, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(CourseAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(ReviewAdmin)
