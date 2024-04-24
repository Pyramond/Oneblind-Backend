from fastapi import APIRouter, Depends
from db.database import SessionLocal
import crud.players as crud
from sqlalchemy.orm import Session
from schemas.players_schema import NewPlayer, Player, PlayerAvatar, Color
from utils.list_avatar import list_avatar


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


@router.post("/player/avatar/update")
def update_avatar(player: PlayerAvatar, db: Session = Depends(get_db)):
    return crud.change_avatar(player.id, player.avatar, db=db)


@router.get("/player/avatar/getAll")
def get_all_avatar():
    return list_avatar()


@router.post("/player/avatar/change_color")
def change_avatar_color(color: Color, db: Session = Depends(get_db)):
    return crud.change_avatar_color(color.userId, color.color, db=db)
