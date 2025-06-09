import datetime

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.app.core.settings import settings
from src.app.db.models import Base
from src.app.db.models.tournament import Tournament, Player
from src.app.main import app

DATABASE_URL = settings.DATABASE_URL

engine_test = create_async_engine(DATABASE_URL, echo=True)
async_session_test = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_test() as session:
        yield session
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_creates_tournament_successfully(client: AsyncClient):
    data = {"name": "Test Tournament", "max_players": 10, "start_at": "2023-12-01T10:00:00"}
    response = await client.post("/tournaments", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == data["name"]
    assert response_data["max_players"] == data["max_players"]
    assert response_data["registered_players"] == 0


@pytest.mark.asyncio
async def test_fails_to_create_tournament_with_invalid_data(client: AsyncClient):
    invalid_data = {"name": "", "max_players": -1, "start_at": "invalid-date"}
    response = await client.post("/tournaments", json=invalid_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_registers_player_successfully(client: AsyncClient, db_session: AsyncSession):
    tournament = Tournament(name="Reg Tournament", max_players=5,
                            start_at=datetime.datetime.fromisoformat("2023-12-01T10:00:00"))
    db_session.add(tournament)
    await db_session.commit()
    await db_session.refresh(tournament)
    await db_session.close()

    data = {"name": "Player 1", "email": "player1@example.com"}
    response = await client.post(f"/tournaments/{tournament.id}/register", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == data["name"]
    assert response_data["email"] == data["email"]


@pytest.mark.asyncio
async def test_fails_to_register_player_when_tournament_full(client: AsyncClient, db_session: AsyncSession):
    tournament = Tournament(name="Full Tournament", max_players=1,
                            start_at=datetime.datetime.fromisoformat("2023-12-01T10:00:00"))
    db_session.add(tournament)
    await db_session.commit()
    await db_session.refresh(tournament)

    existing_player = Player(name="Existing", email="existing@example.com", tournament_id=tournament.id)
    db_session.add(existing_player)
    await db_session.commit()

    new_player = {"name": "New Player", "email": "new@example.com"}
    response = await client.post(f"/tournaments/{tournament.id}/register", json=new_player)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_lists_players_in_tournament(client: AsyncClient, db_session: AsyncSession):
    tournament = Tournament(name="List Tournament", max_players=10,
                            start_at=datetime.datetime.fromisoformat("2023-12-01T10:00:00"))
    db_session.add(tournament)
    await db_session.commit()
    await db_session.refresh(tournament)

    player1 = Player(name="Player 1", email="player1@example.com", tournament_id=tournament.id)
    player2 = Player(name="Player 2", email="player2@example.com", tournament_id=tournament.id)
    db_session.add_all([player1, player2])
    await db_session.commit()

    response = await client.get(f"/tournaments/{tournament.id}/players")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    names = [p["name"] for p in response_data]
    assert "Player 1" in names
    assert "Player 2" in names
