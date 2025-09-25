from fastapi import APIRouter, Depends, BackgroundTasks
from db.database import SessionLocal
import crud.chips as crud
from sqlalchemy.orm import Session
from schemas.chips_schema import NewChip, Chip
from utils.logs import logs


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chips/add")
def add_chips(newChip: NewChip, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return crud.add_chip(newChip.color, newChip.value, db=db)


@router.delete("/chips/remove")
def remove_chips(chip: Chip, db: Session = Depends(get_db)):
    return crud.remove_chip(chip.id, db=db)


@router.get("/chips")
def get_chips(db: Session = Depends(get_db)):
    return crud.get_all_chips(db=db)