from fastapi import APIRouter 

from app.api.routes import q_and_a

api_router = APIRouter()

api_router.include_router(q_and_a.router, prefix="/Q_and_A", tags=["questions and answers"] )
