from pydantic import BaseModel

class NewChip(BaseModel):
    color: str
    value: int

class Chip(BaseModel):
    id: int