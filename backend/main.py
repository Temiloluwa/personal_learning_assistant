from fastapi import fastapi
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)