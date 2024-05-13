import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database import database as database
from database.database import DishDB
from model.model import Dish

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.post("/add_dish")
async def add_dish(dish: Dish, db: db_dependency):
    new_dish = DishDB(**dish.dict())
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


@app.get("/dishes")
async def list_dishes(db: db_dependency):
    return db.query(DishDB).all()


@app.get("/get_dish_by_id/{dish_id}")
async def get_dish_by_id(dish_id: int, db: db_dependency):
    dish = db.query(DishDB).filter(DishDB.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@app.delete("/delete_dish/{dish_id}")
async def delete_dish(dish_id: int, db: db_dependency):
    dish = db.query(DishDB).filter(DishDB.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()
    return {"message": "Dish deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
