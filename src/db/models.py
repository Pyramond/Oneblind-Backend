from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Players(Base):
    __tablename__ = "players_players"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(Integer)
    points = Column(Integer)
    avatar = Column(Integer)
    avatarColor = Column(String)


class BlindModel(Base):
    __tablename__ = "blind_models"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    steps = relationship("BlindSteps", back_populates="model_owner")


class BlindSteps(Base):
    __tablename__ = "blind_steps"

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("blind_models.id"))
    order = Column(Integer)
    type = Column(String)
    time = Column(Integer)
    sb = Column(Integer)

    model_owner = relationship("BlindModel", back_populates="steps")


class Tournament(Base):
    __tablename__ = "tournament_tournament"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(Integer)
    blindName = Column(String)
    blindId = Column(Integer)
    initialChip = Column(Integer)
    state = Column(String)
    points = Column(Integer)

    players = relationship("TournamentPlayer", back_populates="tournament_owner")
    recap = relationship("TournamentRecap", back_populates="tournament_owner")


class TournamentPlayer(Base):
    __tablename__ = "tournament_players"

    id = Column(Integer, primary_key=True)
    Tid = Column(Integer, ForeignKey("tournament_tournament.id"))
    Pid = Column(Integer)
    name = Column(String)
    place = Column(Integer)

    tournament_owner = relationship("Tournament", back_populates="players")


class TournamentRecap(Base):
    __tablename__ = "tournament_recap"

    id = Column(Integer, primary_key=True)
    Tid = Column(Integer, ForeignKey("tournament_tournament.id"))
    avStack = Column(Integer)
    recaveCounter = Column(Integer)
    start = Column(Integer)
    end = Column(Integer)

    tournament_owner = relationship("Tournament", back_populates="recap")
