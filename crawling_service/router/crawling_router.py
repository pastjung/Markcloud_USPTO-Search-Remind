from fastapi import APIRouter
from service import crawling_service

router = APIRouter(
    prefix="/api/crawling",
)

@router.post("/read", response_model=None)
def get_latest():
    crawling_service.get_latest()

@router.post("/read/all", response_model=None)
def get_all():
    crawling_service.get_all()