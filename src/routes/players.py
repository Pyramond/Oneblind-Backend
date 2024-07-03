from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from db.database import SessionLocal
import crud.players as crud
from sqlalchemy.orm import Session
import schemas.players_schema as schemas
from utils.list_avatar import list_avatar
import uuid
from typing import Union


from pathlib import Path


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/player/add")
def add_player(player: schemas.NewPlayer, db: Session = Depends(get_db)):
    return crud.add_player(player.name, player.date, db=db)


@router.get("/player/get_all")
def get_players(db: Session = Depends(get_db)):
    return crud.get_players(db=db)


@router.post("/player/get_id")
def get_id_player(player: schemas.Player, db: Session = Depends(get_db)):
    return crud.get_id_player(id=player.id, db=db)


@router.delete("/player/delete")
def delete_player(player: schemas.Player, db: Session = Depends(get_db)):
    return crud.remove_player(player.id, db=db)


@router.post("/player/avatar/update")
def update_avatar(player: schemas.PlayerAvatar, db: Session = Depends(get_db)):
    return crud.change_avatar(player.id, player.avatar, db=db)


@router.get("/player/avatar/getAll")
def get_all_avatar():
    return list_avatar()


@router.post("/player/avatar/change_color")
def change_avatar_color(color: schemas.Color, db: Session = Depends(get_db)):
    return crud.change_avatar_color(color.userId, color.color, db=db)


@router.post("/player/avatar/upload/")
async def upload_avatar(avatar: UploadFile = File(...), id: int = Form(...), db: Session = Depends(get_db)):

    UPLOAD_DIR = Path("static") / "avatars" / "custom"

    if not avatar.filename.endswith(".png"):
        raise HTTPException(status_code=400, detail="Unauthorized file extension")

    avatar.filename = f"avatar_{id}.png"
    contents = await avatar.read()

    with open(UPLOAD_DIR / avatar.filename, "wb") as f:
        f.write(contents)

    return {"filename": avatar.filename, "msg": "Avatar successfully uploaded"}


@router.post("/player/name/update")
def modifyPlayerName(player: schemas.PlayerName, db: Session = Depends(get_db)):
    return crud.modify_player_name(player.id, player.name, db=db)
