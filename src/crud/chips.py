from sqlalchemy.orm import Session
import db.models as models
from fastapi import HTTPException



def add_chip(color, value, db: Session):

    db_chip = models.Chip(color=color, value=value)
    db.add(db_chip)
    db.commit()
    db.refresh(db_chip)

    return { "msg": "Chip added successfully" }


def remove_chip(id, db: Session):

    chip = db.query(models.Chip).filter(models.Chip.id == id).first()

    if chip:
        db.delete(chip)
        db.commit()
        return { "msg": "Chip removed successfully" }
    else:
        raise HTTPException(status_code=404, detail="Chip not found")


def get_all_chips(db: Session):

    return db.query(models.Chip).all()