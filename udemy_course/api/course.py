from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from udemy_course.db.database import get_db
from udemy_course.db.models import Course
from udemy_course.db.schema import CourseSchema, CourseCreateSchema


course_router = APIRouter(prefix='/course', tags=['Courses'])

@course_router.post('/', response_model=CourseSchema)
async def course_create(course: CourseCreateSchema, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@course_router.get('/', response_model=List[CourseSchema])
async def course_list(db: Session = Depends(get_db)):
    return db.query(Course).all()

@course_router.get('/{course_id}', response_model=CourseSchema)
async def course_detail(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    return db_course

@course_router.put('/{course_id}', response_model=dict)
async def course_update(course_id: int, course: CourseCreateSchema, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    for key, value in course.dict().items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return {'message': 'Updated'}

@course_router.delete('/{course_id}', response_model=dict)
async def course_delete(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail='Course Not Found')
    db.delete(db_course)
    db.commit()
    return {'message': 'Deleted'}
