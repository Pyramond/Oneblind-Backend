from sqlalchemy.orm import Session
import db.models as models


def create_blind_model(name, steps, db: Session):
    db_model = models.BlindModel(name=name)
    db.add(db_model)

    db.commit()
    db.refresh(db_model)

    for step in steps:
        db_step = models.BlindSteps(model_id=db_model.id, order=step.order, type=step.type, time=step.time,
                                    sb=step.SBlind)
        db.add(db_step)
        db.commit()
        db.refresh(db_step)

    return {"msg": "BlindModel added successfully"}


def get_models(db: Session):
    return db.query(models.BlindModel).all()


def delete_model(id, db: Session):
    model = db.query(models.BlindModel).filter(models.BlindModel.id == id).first()
    if model:
        db.delete(model)
        db.query(models.BlindSteps).filter(models.BlindSteps.model_id == id).delete()
        db.commit()
        return {"msg": "Model deleted successfully"}
    else:
        return {"msg": "Model not found"}


def get_id_model(id, db: Session):
    model = db.query(models.BlindModel).filter(models.BlindModel.id == id).first()
    if model:
        steps = []
        for step in model.steps:
            steps.append({
                "order": step.order,
                "type": step.type,
                "time": step.time,
                "sb": step.sb
            })

        return {
            "name": model.name,
            "steps": steps
        }
    else:
        return {"msg": "Model not found"}

