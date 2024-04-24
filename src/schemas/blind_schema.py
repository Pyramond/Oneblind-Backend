from pydantic import BaseModel


class Step(BaseModel):
    order: int
    time: int
    type: str
    SBlind: int


class NewBlindModel(BaseModel):
    name: str
    steps: list[Step]


class Model(BaseModel):
    id: int
