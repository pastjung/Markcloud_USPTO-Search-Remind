from fastapi import APIRouter, Query
from typing import Optional

from service import mongo_search_service
from schema import mongo_search_schema

router = APIRouter(
    prefix="/api/search/mongodb",
)

@router.get("/serial-number/{serial-number}")
def search_by_serialNumber(serial_number : str):
    return mongo_search_service.search_by_serialNumber(serial_number)

@router.get("/registration-number/{registration_number}")
def search_by_registrationNumber(registration_number : str):
    return mongo_search_service.search_by_registrationNumber(registration_number)

@router.get("/case-file-header/filing-date")
def search_by_filingDate(start_date : str, end_date : str, 
                         page: int = Query(1, ge=1), size : int = Query(10, le=50)):
    return mongo_search_service.search_by_filingDate(start_date, end_date, page, size)

@router.get("/case-file-header/filing-date/ordered/by/employee-name")
def ordered_search_by_filingDate(
    start_date: str, 
    end_date: str, 
    page: int = Query(1, ge=1), 
    size: int = Query(10, le=50),
    sort_order: Optional[int] = Query(1)    # 정렬 방향 -> 1 : 오름차순, -1 : 내임차순
):
    return mongo_search_service.ordered_search_by_filingDate(start_date, end_date, page, size, sort_order)

@router.get("/mark-identification", response_model=mongo_search_schema.Uspto)
def search_by_markIdentification(workmark: str):
    return mongo_search_service.search_by_mark_identification(workmark)