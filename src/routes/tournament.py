from fastapi import APIRouter, Depends
from database import engine, SessionLocal
import crud
from sqlalchemy.orm import Session
from routes.schemas.tournament_schema import NewTournament, Tournament, ElPlayer


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tournament/create")
def create_tournament(tournament: NewTournament, db: Session = Depends(get_db)):
    return crud.create_tournament(tournament, db=db)


@router.get("/tournament/get_all")
def get_all_tournaments(db: Session = Depends(get_db)):
    return crud.get_all_tournaments("all", db=db)


@router.get("/tournament/get_currents")
def get_currents(db: Session = Depends(get_db)):
    return crud.get_all_tournaments("current", db=db)


@router.post("/tournament/get_players")
def get_tournament_players(tournament: Tournament, db: Session = Depends(get_db)):
    return crud.get_tournament_players(tournament.id, db=db)


@router.post("/tournament/delete")
def delete_tournament(tournament: Tournament, db: Session = Depends(get_db)):
    return crud.delete_tournament(tournament.id, db=db)


@router.post("/tournament/get_id")
def get_id_tournament(tournament: Tournament, db: Session = Depends(get_db)):
    return crud.get_id_tournament(tournament.id, db=db)


@router.post("/tournament/eliminate")
def eliminate(elPlayer: ElPlayer, db: Session = Depends(get_db)):
    points_func = crud.set_points(elPlayer.points, elPlayer.id, db=db)
    place_func = crud.set_place(elPlayer.place, elPlayer.tournament, elPlayer.id, db=db)
    return {
        "place": place_func,
        "points": points_func
    }


@router.post("/tournament/get_player_tournaments")
def get_player_tournaments(player: Tournament, db: Session = Depends(get_db)):
    return crud.get_player_tournaments(player.id, db=db)


@router.post("/tournament/delete/force")
def force_delete_tournament(tournament: Tournament, db: Session = Depends(get_db)):
    return crud.force_delete_tournament(tournament.id, db=db)
