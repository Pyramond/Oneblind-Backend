from sqlalchemy.orm import Session
import db.models as models
from fastapi import HTTPException, UploadFile
from pathlib import Path


def add_player(name, date, db: Session):
    db_user = models.Players(name=name, date=date, points=0, avatar=-1, avatarColor="108cd0")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_avatar(id, avatar, db: Session):
    player = db.query(models.Players).filter(models.Players.id == id).first()
    if player:
        player.avatar = avatar
        db.commit()
        db.refresh(player)
        return {"msg": "Avatar updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Player not found")


def remove_player(id, db: Session):
    player = db.query(models.Players).filter(models.Players.id == id).first()
    if player:
        db.delete(player)
        db.commit()
        return {"msg": "Player deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")


def get_id_player(id, db: Session):
    return db.query(models.Players).filter(models.Players.id == id).first()


def get_players(db: Session):
    return db.query(models.Players).all()


def change_avatar_color(id, color, db: Session):
    player = db.query(models.Players).filter(models.Players.id == id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.avatarColor = color
    db.commit()
    db.refresh(player)
    return {"msg": "Color successfully updated"}


def modify_player_name(id, name, db: Session):
    player = db.query(models.Players).filter(models.Players.id == id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.name = name
    db.commit()
    db.refresh(player)

    return {"msg": "Player's name updated successfully"}
