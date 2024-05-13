import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from sqlalchemy.orm import Session
from typing import Annotated

from database import database as database
from database.database import DishDB
from model.model import Dish
from keycloak import KeycloakOpenID

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/sign_in")
async def sign_in(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def check_for_role(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (check_for_role(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_dish")
async def add_dish(dish: Dish, db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        new_dish = DishDB(**dish.dict())
        db.add(new_dish)
        db.commit()
        db.refresh(new_dish)
        return new_dish
    else:
        return "Wrong JWT Token"


@app.get("/dishes")
async def list_dishes(db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        return db.query(DishDB).all()
    else:
        return "Wrong JWT Token"


@app.get("/get_dish_by_id/{dish_id}")
async def get_dish_by_id(dish_id: int, db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        dish = db.query(DishDB).filter(DishDB.id == dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        return dish
    else:
        return "Wrong JWT Token"


@app.delete("/delete_dish/{dish_id}")
async def delete_dish(dish_id: int, db: db_dependency, token: str = Header()):
    if (check_for_role(token)):
        dish = db.query(DishDB).filter(DishDB.id == dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        db.delete(dish)
        db.commit()
        return {"message": "Dish deleted successfully"}
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
