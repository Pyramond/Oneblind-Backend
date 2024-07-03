from pydantic import BaseModel


class NewPlayer(BaseModel):
    name: str
    date: int


class Player(BaseModel):
    id: int


class PlayerAvatar(BaseModel):
    id: int
    avatar: int


class Color(BaseModel):
    userId: int
    color: str


class PlayerName(BaseModel):
    id: int
    name: str
