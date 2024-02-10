from fastapi import APIRouter
from os import remove
import models
from database import engine


router = APIRouter()


@router.delete("/database")
def delete_database():
    try:
        remove("./static/database.db")
        models.Base.metadata.create_all(bind=engine)
        return {"msg": "Database successfully reset"}
    except FileNotFoundError:
        return {"msg": "Internal server error"}
