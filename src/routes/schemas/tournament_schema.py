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
