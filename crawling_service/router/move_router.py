from fastapi import APIRouter
from service import move_service

router = APIRouter(
    prefix="/api/move",
)
    
@router.post("/to/elsticsearch", response_model=None)
def move_to_elasticsearch():
    move_service.move_to_elasticsearch()