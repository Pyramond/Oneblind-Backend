from fastapi import APIRouter, Depends, BackgroundTasks
from db.database import SessionLocal
import crud.tournament as crud
from sqlalchemy.orm import Session
from schemas.tournament_schema import NewTournament, Tournament, ElPlayer, NewTournamentPlayer, Recap, UpdateTournament
from utils.logs import logs


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tournament/create")
def create_tournament(background_tasks: BackgroundTasks, tournament: NewTournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/create", 200)
    return crud.create_tournament(tournament, db=db)


@router.get("/tournament/get_all")
def get_all_tournaments(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "GET /tournament/get_all", 200)
    return crud.get_all_tournaments("all", db=db)


@router.get("/tournament/get_currents")
def get_currents(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "GET /tournament/get_currents", 200)
    return crud.get_all_tournaments("current", db=db)


@router.post("/tournament/get_players")
def get_tournament_players(background_tasks: BackgroundTasks, tournament: Tournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/get_players", 200)
    return crud.get_tournament_players(tournament.id, db=db)


@router.post("/tournament/delete")
def delete_tournament(background_tasks: BackgroundTasks, tournament: Tournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/delete", 200)
    return crud.delete_tournament(tournament.id, db=db)


@router.post("/tournament/get_id")
def get_id_tournament(background_tasks: BackgroundTasks, tournament: Tournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/get_id", 200)
    return crud.get_id_tournament(tournament.id, db=db)


@router.post("/tournament/eliminate")
def eliminate(background_tasks: BackgroundTasks, elPlayer: ElPlayer, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/eliminate", 200)
    points_func = crud.set_points(elPlayer.points, elPlayer.id, db=db)
    place_func = crud.set_place(elPlayer.place, elPlayer.tournament, elPlayer.id, db=db)
    return {
        "place": place_func,
        "points": points_func
    }


@router.post("/tournament/get_player_tournaments")
def get_player_tournaments(background_tasks: BackgroundTasks, player: Tournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/get_player_tournaments", 200)
    return crud.get_player_tournaments(player.id, db=db)


@router.post("/tournament/delete/force")
def force_delete_tournament(background_tasks: BackgroundTasks, tournament: Tournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/delete/force", 200)
    return crud.force_delete_tournament(tournament.id, db=db)


@router.post("/tournament/add/player")
def add_player_tournament(background_tasks: BackgroundTasks, player: NewTournamentPlayer, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/add/player", 200)
    return crud.add_player_tournament(player.Pid, player.Tid, db=db)


@router.post("/tournament/remove/player")
def remove_player_tournament(background_tasks: BackgroundTasks, player: NewTournamentPlayer, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/remove/player", 200)
    return crud.remove_player_tournament(player.Pid, player.Tid, db=db)


@router.post("/tournament/recap/create")
def create_tournament_recap(background_tasks: BackgroundTasks, recap: Recap, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/recap/create", 200)
    return crud.create_tournament_recap(recap.Tid, recap.avStack, recap.recaveCounter, recap.start, recap.end, db=db)


@router.post("/tournament/recap/get")
def get_tournament_recap(background_tasks: BackgroundTasks, tournament: Tournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/recap/get", 200)
    return crud.get_tournament_recap(tournament.id, db=db)


@router.post("/tournament/update")
def update_tournament(background_tasks: BackgroundTasks, tournamentInfos: UpdateTournament, db: Session = Depends(get_db)):
    background_tasks.add_task(logs, "POST /tournament/update", 200)
    return crud.update_tournament_infos(tournamentInfos.Tid, tournamentInfos.name, tournamentInfos.points, tournamentInfos.initialChips, tournamentInfos.blindName, tournamentInfos.blindId, db=db)
