from fastapi import APIRouter, Depends, BackgroundTasks
from db.database import SessionLocal
import crud.database as crud
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


@router.get("/database/remove_points")
def database_remove_points(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return crud.remove_points(db=db)