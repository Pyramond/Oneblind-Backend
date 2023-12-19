from pydantic import BaseModel


class NewPlayer(BaseModel):
    name: str
    date: int


class Player(BaseModel):
    id: int
    