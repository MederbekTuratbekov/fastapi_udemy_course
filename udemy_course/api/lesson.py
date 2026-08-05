from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from udemy_course.db.database import get_db
from udemy_course.db.models import Lesson
from udemy_course.db.schema import LessonSchema, LessonCreateSchema


lesson_router = APIRouter(prefix='/lesson', tags=['Lesson'])

@lesson_router.post('/', response_model=LessonSchema)
async def lesson_create(lesson: LessonCreateSchema, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@lesson_router.get('/', response_model=List[LessonSchema])
async def lesson_list(db: Session = Depends(get_db)):
    return db.query(Lesson).all()

@lesson_router.get('/{lesson_id}', response_model=LessonSchema)
async def lesson_detail(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail='Lesson Not Found')
    return db_lesson

@lesson_router.put('/{lesson_id}', response_model=dict)
async def lesson_update(lesson_id: int, lesson: LessonCreateSchema, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail='Lesson Not Found')
    for key, value in lesson.dict().items():
        setattr(db_lesson, key, value)
    db.commit()
    db.refresh(db_lesson)
    return {'message': 'Updated'}

@lesson_router.delete('/{lesson_id}', response_model=dict)
async def lesson_delete(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if db_lesson is None:
        raise HTTPException(status_code=404, detail='Lesson Not Found')
    db.delete(db_lesson)
    db.commit()
    return {'message': 'Deleted'}
