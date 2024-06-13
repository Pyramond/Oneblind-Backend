from sqlalchemy.orm import Session
import db.models as models
from fastapi import HTTPException


def create_tournament(tournament, db: Session):
    points = 0
    if tournament.points: points = 1

    db_tournament = models.Tournament(name=tournament.name, date=tournament.date, initialChip=tournament.initialChips,
                                      state="current", blindName=tournament.blind.name, blindId=tournament.blind.id,
                                      points=points)
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
        raise HTTPException(status_code=400, detail="Incorrect state")


def get_tournament_players(id, db: Session):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if tournament:
        players = []

        for player in tournament.players:
            players.append({
                "name": player.name,
                "id": player.Pid
            })

        return players
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")


def delete_tournament(id, db: Session):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if db_tournament:
        db_tournament.state = "old"
        db.commit()
        db.refresh(db_tournament)

        return {"msg": "Tournament deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")


def get_id_tournament(id, db: Session):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

    if db_tournament:
        return {
            "id": db_tournament.id,
            "name": db_tournament.name,
            "date": db_tournament.date,
            "blindName": db_tournament.blindName,
            "blindId": db_tournament.blindId,
            "initialChip": db_tournament.initialChip,
            "points": db_tournament.points
        }
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")


def set_points(points, id, db: Session):
    db_player = db.query(models.Players).filter(models.Players.id == id).first()

    if db_player:
        db_player.points = db_player.points + points
        db.commit()
        db.refresh(db_player)
        return {"msg": "Points added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Player not found")


def set_place(place, Tid, Pid, db: Session):
    db_player = db.query(models.TournamentPlayer).filter(
        (models.TournamentPlayer.Pid == Pid) & (models.TournamentPlayer.Tid == Tid)).first()
    if db_player:
        db_player.place = place
        db.commit()
        db.refresh(db_player)
        return {"msg": "Place added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")


def get_player_tournaments(id, db: Session):
    db_player = db.query(models.TournamentPlayer.Tid, models.TournamentPlayer.place).filter(
        models.TournamentPlayer.Pid == id).all()

    if db_player:
        data = []

        for elt in db_player:
            db_tournament = db.query(models.Tournament.name, models.Tournament.date).filter(
                models.Tournament.id == elt[0]).all()
            data.append({
                "id": elt[0],
                "place": elt[1],
                "name": db_tournament[0][0],
                "date": db_tournament[0][1]
            })

        return data

    else:
        raise HTTPException(status_code=404, detail="Player not found")


def force_delete_tournament(id, db: Session):
    tournamentPlayers = db.query(models.TournamentPlayer).filter(models.TournamentPlayer.Tid == id).all()
    if tournamentPlayers:

        for player in tournamentPlayers:
            db.delete(player)
            db.commit()

        tournament = db.query(models.Tournament).filter(models.Tournament.id == id).first()

        if tournament:
            db.delete(tournament)
            db.commit()

            return {"msg": "Tournament successfully deleted"}
        else:
            raise HTTPException(status_code=404, detail="Tournament not found")
    else:
        raise HTTPException(status_code=404, detail="Tournament players not found")


def add_player_tournament(Pid, Tid, db: Session):
    player = db.query(models.Players).filter(models.Players.id == Pid).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    tournament = db.query(models.Tournament).filter(models.Tournament.id == Tid).first()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    elif tournament.state == "old":
        return {"msg": "This tournament is already finished"}

    isAlreadyAdded = db.query(models.TournamentPlayer).filter(
        (models.TournamentPlayer.Tid == Tid) & (models.TournamentPlayer.Pid == Pid)).first()

    if isAlreadyAdded:
        raise HTTPException(status_code=409, detail="This player is already added to this tournament")

    db_playerTournament = models.TournamentPlayer(Tid=Tid, Pid=Pid, name=player.name, place=0)
    db.add(db_playerTournament)
    db.commit()
    db.refresh(db_playerTournament)
    return {"msg": "Player successfully added to this tournament"}


def remove_player_tournament(Pid, Tid, db: Session):
    player = db.query(models.Players).filter(models.Players.id == Pid).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    tournament = db.query(models.Tournament).filter(models.Tournament.id == Tid).first()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    elif tournament.state == "old":
        raise HTTPException(status_code=409, detail="This tournament is already finished")

    isAlreadyAdded = db.query(models.TournamentPlayer).filter(
        (models.TournamentPlayer.Tid == Tid) & (models.TournamentPlayer.Pid == Pid)).first()

    if not isAlreadyAdded:
        raise HTTPException(status_code=409, detail="This player is not in this tournament")

    db.delete(isAlreadyAdded)
    db.commit()

    return {"msg": "Player successfully removed to this tournament"}


def create_tournament_recap(Tid, avStack, recaveCounter, start, end, db: Session):
    recap = db.query(models.TournamentRecap).filter(models.TournamentRecap.Tid == Tid).first()

    if recap:

        recap.avStack = avStack
        recap.recaveCounter = recaveCounter
        recap.start = start
        recap.end = end

        db.commit()
        db.refresh(recap)

        return {"msg": "Tournament recap successfully updated"}

    else:

        db_recap = models.TournamentRecap(Tid=Tid, avStack=float(avStack), recaveCounter=recaveCounter, start=start,
                                          end=end)
        db.add(db_recap)
        db.commit()
        db.refresh(db_recap)

        return {"msg": "Tournament recap successfully created"}


def get_tournament_recap(Tid, db: Session):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == Tid).first()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    recap = db.query(models.TournamentRecap).filter(models.TournamentRecap.Tid == Tid).first()

    if not recap:
        raise HTTPException(status_code=404, detail="Tournament recap not found")

    players = db.query(models.TournamentPlayer).filter(models.TournamentPlayer.Tid == Tid).all()

    if not players:
        raise HTTPException(status_code=409, detail="There is no players in this tournament")

    return {
        "recap": recap,
        "players": players,
        "tournament": tournament
    }
