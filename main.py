from typing import Annotated

from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, LocalSession
import model

api = FastAPI()

model.base.metadata.create_all(bind=engine)

items = []

class Item(BaseModel):
    Task: str
    Status: bool = False

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@api.get("/")
def read_root():
    return {"hello": "world"}

@api.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: db_dependency):
    item = db.query(model.To_do).filter(model.To_do.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail='Item Not Found')
    else:
        return item

@api.post("/items", status_code=status.HTTP_201_CREATED)
def add_items(item: Item, db: db_dependency):
    db_item = model.To_do(**item.model_dump())
    db.add(db_item)
    db.commit()
    items.append(item)
    return items

@api.get("/items", status_code=status.HTTP_200_OK)
def read_items(db: db_dependency):
    return db.query(model.To_do).filter(model.To_do.id is not None).all()

@api.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
async def delete_items(item_id: int, db: db_dependency):
    item = db.query(model.To_do).filter(model.To_do.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="The asked ID does not exist")
    else:
        db.delete(item)
        db.commit()
