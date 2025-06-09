from src.app.api import tournament
from src.app.asgi import application

app = application()
app.include_router(tournament.router)
