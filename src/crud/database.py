from sqlalchemy.orm import Session
import db.models as models
from fastapi import HTTPException


def remove_points(db: Session):

    players = db.query(models.Players).all()

    if players:
        for player in players:
            player.points = 0
            db.commit()
            db.refresh(player)
    else:
        raise HTTPException(status_code=404, detail="Players not found")

    return { "msg": "Players's points successfully removed" }