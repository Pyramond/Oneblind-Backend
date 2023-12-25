from sqlalchemy.orm import Session
import models


# PLAYERS
def get_players(db: Session):
    return db.query(models.Players).all()


def add_player(name, date, db: Session):
    db_user = models.Players(name=name, date=date, points=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_player(id, db: Session):
    player = db.query(models.Players).filter(models.Players.id == id).first()
    if player:
        db.delete(player)
        db.commit()
        return {"msg": "Player deleted successfully"}
    else:
        return {"msg": "Tournament Not Found"}


def get_id_player(id, db: Session):
    return db.query(models.Players).filter(models.Players.id == id).first()


# BlindModel
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


# Tournament
def create_tournament(tournament, db: Session):
    db_tournament = models.Tournament(name=tournament.name, date=tournament.date, initialChip=tournament.initialChips,
                                      state="current", blindName=tournament.blind.name, blindId=tournament.blind.id)
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)

    for player in tournament.players:
        db_player = models.TournamentPlayer(Tid=db_tournament.id, Pid=player.id, name=player.name, place=0)
        db.add(db_player)
        db.commit()
        db.refresh(db_player)

    return {"msg": "Tournament added successfully"}


def get_all_tournaments(state, db: Session):

    result = None
    if state == "all":
        result = db.query(models.Tournament).all()
    elif state == "current":
        result = db.query(models.Tournament).filter(models.Tournament.state == "current").all()
    elif state == "old":
        result = db.query(models.Tournament).filter(models.Tournament.state == "old").all()

    if result is not None:
        tournaments = []

        for elt in result:
            tournaments.append({
                "id": elt.id,
                "name": elt.name,
                "date": elt.date,
                "blindName": elt.blindName,
                "blindId": elt.blindId,
                "initialChip": elt.initialChip,
                "state": elt.state
            })
        return tournaments
    elif result is None:
        return {"msg": "Error: Incorrect state"}


def get_tournament_players(id, db: Session):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if tournament:
        players = []

        for player in tournament.players:
            players.append({
                "name": player.name,
                "id": player.id
            })

        return players
    else:
        return {"msg": "Tournament Not Found"}


def delete_tournament(id, db: Session):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if db_tournament:
        db_tournament.state = "old"
        db.commit()
        db.refresh(db_tournament)

        return {"msg": "Tournament deleted successfully"}
    else:
        return {"msg": "Tournament Not Found"}


def get_id_tournament(id, db: Session):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if db_tournament:
        return {
            "id": db_tournament.id,
            "name": db_tournament.name,
            "date": db_tournament.date,
            "blindName": db_tournament.blindName,
            "blindId": db_tournament.blindId,
            "initialChip": db_tournament.initialChip
        }
    else:
        return {"msg": "Tournament Not Found"}


def set_points(points, id, db: Session):
    db_player = db.query(models.Players).filter(models.Players.id == id).first()

    if db_player:
        db_player.points = db_player.points + points
        db.commit()
        db.refresh(db_player)
        return {"msg": "Points added successfully"}
    else:
        return {"msg": "Player Not Found"}


def set_place(place, Tid, Pid, db: Session):
    db_player = db.query(models.TournamentPlayer).filter((models.TournamentPlayer.Pid == Pid) & (models.TournamentPlayer.Tid == Tid)).first()
    if db_player:
        db_player.place = place
        db.commit()
        db.refresh(db_player)
        return {"msg": "Place added successfully"}
    else:
        return {"msg": "Tournament Not Found"}


def get_player_tournaments(id, db: Session):
    db_player = db.query(models.TournamentPlayer.Tid, models.TournamentPlayer.place).filter(models.TournamentPlayer.Pid == id).all()

    if db_player:
        data = []

        for elt in db_player:
            db_tournament = db.query(models.Tournament.name, models.Tournament.date).filter(models.Tournament.id == elt[0]).all()
            data.append({
                "id": elt[0],
                "place": elt[1],
                "name": db_tournament[0][0],
                "date": db_tournament[0][1]
            })

        return data

    else:
        return {"msg": "Player Not Found"}


def force_delete_tournament(id, db: Session):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if tournament:
        db.delete(tournament)
        db.commit()
        return {"msg": "Tournament successfully deleted"}
    else:
        return {"msg": "Tournament Not Found"}