from fastapi import APIRouter, Depends
from db.database import SessionLocal
import crud.blind_model as crud
from sqlalchemy.orm import Session
from schemas.blind_schema import NewBlindModel, Model


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/blind/add")
def add_blind_model(newBlindModel: NewBlindModel, db: Session = Depends(get_db)):
    return crud.create_blind_model(newBlindModel.name, newBlindModel.steps, db=db)


@router.get("/blind/get_models")
def get_model(db: Session = Depends(get_db)):
    return crud.get_models(db=db)


@router.post("/blind/delete")
def delete_model(model: Model, db: Session = Depends(get_db)):
    return crud.delete_model(model.id, db=db)


@router.post("/blind/get_id")
def get_id_model(model: Model, db: Session = Depends(get_db)):
    return crud.get_id_model(model.id, db=db)
