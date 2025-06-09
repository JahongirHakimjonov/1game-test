from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    max_players = Column(Integer, nullable=False)
    start_at = Column(DateTime, nullable=False)
    players = relationship("Player", back_populates="tournament")


class Player(Base):
    __tablename__ = "players"
    __table_args__ = (
        UniqueConstraint("tournament_id", "email", name="uq_tournament_email"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    tournament = relationship("Tournament", back_populates="players")
