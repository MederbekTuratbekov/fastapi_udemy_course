from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from udemy_course.db.models import Category
from udemy_course.db.schema import CategorySchema, CategoryCreateSchema
from udemy_course.db.database import get_db


category_router = APIRouter(prefix='/category', tags=['Categories'])

@category_router.post('/', response_model=CategorySchema)
async def category_create(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@category_router.get('/', response_model=List[CategorySchema])
async def category_list(db: Session = Depends(get_db)):
    return db.query(Category).all()

@category_router.get('/{category_id}', response_model=CategorySchema)
async def category_detail(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    return db_category

@category_router.put('/{category_id}', response_model=dict)
async def category_update(category_id: int, category: CategoryCreateSchema, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    db_category.category_name = category.category_name
    db.commit()
    db.refresh(db_category)
    return {'message': 'Updated'}

@category_router.delete('/{category_id}', response_model=dict)
async def category_delete(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    db.delete(db_category)
    db.commit()
    return {'message': 'Deleted'}
