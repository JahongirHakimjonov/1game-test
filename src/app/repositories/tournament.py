import datetime

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.tournament import Tournament, Player


async def create_tournament(db: AsyncSession, data):
    tournament_data = data.dict()
    start_at = tournament_data.get("start_at")
    if start_at and start_at.tzinfo is not None:
        tournament_data["start_at"] = start_at.astimezone(
            datetime.timezone.utc
        ).replace(tzinfo=None)
    tournament = Tournament(**tournament_data)
    db.add(tournament)
    await db.commit()
    await db.refresh(tournament)
    return tournament


async def register_player(db: AsyncSession, tournament_id: int, data):
    result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    tournament = result.scalar_one_or_none()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    player_count = await db.scalar(
        select(func.count(Player.id)).where(Player.tournament_id == tournament_id)
    )
    if player_count >= tournament.max_players:
        raise HTTPException(status_code=400, detail="Player limit reached")

    player = Player(name=data.name, email=data.email, tournament_id=tournament_id)
    db.add(player)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Player already registered")
    return player


async def list_players(db: AsyncSession, tournament_id: int):
    result = await db.execute(
        select(Player).where(Player.tournament_id == tournament_id)
    )
    return result.scalars().all()
