from fastapi import FastAPI
import uvicorn
from udemy_course.api import category, course, lesson, review, auth, social_auth
from udemy_course.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from udemy_course.config import SECRET_KEY


udemy = FastAPI()
udemy.include_router(category.category_router)
udemy.include_router(course.course_router)
udemy.include_router(lesson.lesson_router)
udemy.include_router(review.review_router)
udemy.include_router(auth.auth_router)
udemy.include_router(social_auth.social_router)
udemy.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
setup_admin(udemy)


if __name__ == '__main__':
    uvicorn.run(udemy, host='127.0.0.1', port=8000)
