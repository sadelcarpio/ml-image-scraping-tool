from fastapi import FastAPI, Depends
from sqlmodel import Session

from app.api.deps import get_db
from app.core.config import settings

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/healthcheck")
def healthcheck(session: Session = Depends(get_db)):
    return "ok"
