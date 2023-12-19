from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import players, blind_models, tournament
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(players.router)
app.include_router(blind_models.router)
app.include_router(tournament.router)
