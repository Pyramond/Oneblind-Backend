from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from db.database import SessionLocal
import crud.players as crud
from sqlalchemy.orm import Session
import schemas.players_schema as schemas
from utils.list_avatar import list_avatar
from utils.logs import logs
from pathlib import Path


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/player/add")
def add_player(player: schemas.NewPlayer, background_tasks: BackgroundTasks,  db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /player/add", 200, player.name)
    return crud.add_player(player.name, player.date, db=db)


@router.get("/player/get_all")
def get_players(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "GET /player/get_all", 200)
    return crud.get_players(db=db)


@router.post("/player/get_id")
def get_id_player(background_tasks: BackgroundTasks, player: schemas.Player, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /player/get_id", 200, player.id)
    return crud.get_id_player(id=player.id, db=db)


@router.delete("/player/delete")
def delete_player(background_tasks: BackgroundTasks, player: schemas.Player, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "DELETE /player/delete", 200)
    res = crud.remove_player(player.id, db=db)
    return res.status


@router.post("/player/avatar/update")
def update_avatar(background_tasks: BackgroundTasks, player: schemas.PlayerAvatar, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /player/avatar/update", 200, player.id)
    return crud.change_avatar(player.id, player.avatar, db=db)


@router.get("/player/avatar/getAll")
def get_all_avatar(background_tasks: BackgroundTasks):
    background_tasks.add_task(logs, "GET /player/avatar/getAll", 200)
    return list_avatar()


@router.post("/player/avatar/change_color")
def change_avatar_color(background_tasks: BackgroundTasks, color: schemas.Color, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /player/avatar/change_color", 200, color.userId)
    return crud.change_avatar_color(color.userId, color.color, db=db)


@router.post("/player/avatar/upload/")
async def upload_avatar(background_tasks: BackgroundTasks, avatar: UploadFile = File(...), id: int = Form(...), db: Session = Depends(get_db)):

    UPLOAD_DIR = Path("static") / "avatars" / "custom"

    if not avatar.filename.endswith(".png"):
        raise HTTPException(status_code=400, detail="Unauthorized file extension")

    avatar.filename = f"avatar_{id}.png"
    contents = await avatar.read()

    with open(UPLOAD_DIR / avatar.filename, "wb") as f:
        f.write(contents)

    background_tasks.add_task(logs, "POST /player/avatar/upload", 200, id)
    return {"filename": avatar.filename, "msg": "Avatar successfully uploaded"}


@router.post("/player/name/update")
def modifyPlayerName(background_tasks: BackgroundTasks, player: schemas.PlayerName, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /player/name/update", 200, player.id)
    return crud.modify_player_name(player.id, player.name, db=db)
