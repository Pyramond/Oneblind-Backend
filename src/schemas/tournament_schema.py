from pydantic import BaseModel


class BlindModel(BaseModel):
    name: str
    id: int


class Player(BaseModel):
    id: int
    name: str
    date: int
    points: int


class NewTournament(BaseModel):
    blind: BlindModel
    date: int
    initialChips: int
    name: str
    players: list[Player]
    points: bool


class Tournament(BaseModel):
    id: int


class ElPlayer(BaseModel):
    id: int
    place: int
    tournament: int
    points: int


class TournamentPlayer(BaseModel):
    id: int


class NewTournamentPlayer(BaseModel):
    Pid: int
    Tid: int


class Recap(BaseModel):
    Tid: int
    avStack: str
    recaveCounter: int
    start: int
    end: int


class UpdateTournament(BaseModel):
    name: str
    initialChips: int
    blindName: str
    blindId: int
    points: bool
    Tid: int
