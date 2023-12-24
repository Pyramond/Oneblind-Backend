from fastapi import APIRouter, Depends
from database import engine, SessionLocal
import crud
from sqlalchemy.orm import Session
from routes.schemas.players_schema import NewPlayer, Player

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/player/add")
def add_player(player: NewPlayer, db: Session = Depends(get_db)):
    return crud.add_player(player.name, player.date, db=db)


@router.get("/player/get_all")
def get_players(db: Session = Depends(get_db)):
    return crud.get_players(db=db)


@router.post("/player/get_id")
def get_id_player(player: Player, db: Session = Depends(get_db)):
    return crud.get_id_player(id=player.id, db=db)


@router.delete("/player/delete")
def delete_player(player: Player, db: Session = Depends(get_db)):
    return crud.remove_player(player.id, db=db)