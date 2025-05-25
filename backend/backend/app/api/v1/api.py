from fastapi import APIRouter
from app.api.v1.endpoints import availability

api_router = APIRouter()
api_router.include_router(
    availability.router,
    prefix="/availability",
    tags=["availability"],
    responses={404: {"description": "Not found"}}
) 