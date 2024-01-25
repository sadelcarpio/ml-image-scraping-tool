from app import create_app
from app.core.config import Settings
from app.db.init_db import init_db

app = create_app(settings=Settings())
init_db()
