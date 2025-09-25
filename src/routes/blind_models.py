from fastapi import APIRouter, Depends, BackgroundTasks
from db.database import SessionLocal
import crud.blind_model as crud
from sqlalchemy.orm import Session
from schemas.blind_schema import NewBlindModel, Model
from utils.logs import logs


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/blind/add")
def add_blind_model(background_tasks: BackgroundTasks, newBlindModel: NewBlindModel, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /blind/add", 200)
    return crud.create_blind_model(newBlindModel.name, newBlindModel.steps, db=db)


@router.get("/blind/get_models")
def get_model(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "GET /blind/get_models", 200)
    return crud.get_models(db=db)


@router.post("/blind/delete")
def delete_model(background_tasks: BackgroundTasks, model: Model, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /blind/delete", 200)
    return crud.delete_model(model.id, db=db)


@router.post("/blind/get_id")
def get_id_model(background_tasks: BackgroundTasks, model: Model, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /blind/get_id", 200)
    return crud.get_id_model(model.id, db=db)
