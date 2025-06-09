from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.database import SessionLocal
from src.app.db.models.tournament import Player
from src.app.repositories import tournament as repo
from src.app.schemas import tournament as schemas

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/tournaments", response_model=schemas.TournamentOut)
async def create(data: schemas.TournamentCreate, db: AsyncSession = Depends(get_db)):
    tournament = await repo.create_tournament(db, data)
    result = await db.execute(
        select(func.count(Player.id)).where(Player.tournament_id == tournament.id)
    )
    registered = result.scalar_one()
    return schemas.TournamentOut(
        id=tournament.id,
        name=tournament.name,
        max_players=tournament.max_players,
        start_at=tournament.start_at,
        registered_players=registered,
    )


@router.post("/tournaments/{tournament_id}/register")
async def register(
    tournament_id: int, data: schemas.PlayerCreate, db: AsyncSession = Depends(get_db)
):
    player = await repo.register_player(db, tournament_id, data)
    return {"name": player.name, "email": player.email}


@router.get(
    "/tournaments/{tournament_id}/players", response_model=list[schemas.PlayerOut]
)
async def list_players(tournament_id: int, db: AsyncSession = Depends(get_db)):
    return await repo.list_players(db, tournament_id)
