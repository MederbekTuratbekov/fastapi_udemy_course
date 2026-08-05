from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from udemy_course.db.database import get_db
from udemy_course.db.models import Review
from udemy_course.db.schema import ReviewSchema, ReviewCreateSchema


review_router = APIRouter(prefix='/review', tags=['Review'])

@review_router.post('/', response_model=ReviewSchema)
async def review_create(review: ReviewCreateSchema, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@review_router.get('/', response_model=List[ReviewSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get('/{review_id}', response_model=ReviewSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    return db_review

@review_router.put('/{review_id}', response_model=dict)
async def review_update(review_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    for key, value in review.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return {'message': 'Updated'}

@review_router.delete('/{review_id}', response_model=dict)
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    db.delete(db_review)
    db.commit()
    return {'message': 'Deleted'}
