from fastapi import APIRouter, HTTPException
from service import es_search_service

router = APIRouter(
    prefix="/api/search/elasticsearch",
)
    
@router.get("/find")
def find_data_from_elasticsearch(workmark: str, sort_method: int = 1, sort_order:int = 1):
    try:
        results = es_search_service.find_data_from_elasticsearch(workmark, sort_method, sort_order)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
@router.get("/find/all")
def find_all_data_from_elasticsearch(sort_method: int = 1, sort_order: int = 1):
    try:
        results = es_search_service.find_all_data_from_elasticsearch(sort_method, sort_order)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))