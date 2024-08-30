from fastapi import HTTPException 
from typing import Dict, Any

from core.database import collection

def search_query(query : str):
    doc = collection.find_one(query)
    
    if doc is None:
        raise HTTPException(status_code=404, detail="Document Not Found")
    doc.pop("_id", None)
    return doc
    
def search_query_list(query : str, page : int, size : int) -> Dict[str, Any]:
    skip = (page -1) * size
    cursor = collection.find(query).skip(skip).limit(size)
    docs = list(cursor)
    
    total_count = collection.count_documents(query)
    
    if docs is None:
        raise HTTPException(status_code=404, detail="Document Not Found")
    
    for doc in docs:
        doc.pop("_id", None)
        
    return {
        "page": page,
        "per_page": size,
        "total_results": total_count,
        "total_pages": (total_count + size - 1) // size,
        "data": docs
    }
    
def ordered_search_query_list(
    query: Dict[str, Any], 
    page: int, 
    size: int, 
    sort_order: int
) -> Dict[str, Any]:
    skip = (page - 1) * size
    cursor = collection.find(query).skip(skip).limit(size).sort("case-file-header.employee-name", sort_order)
    docs = list(cursor)
    
    total_count = collection.count_documents(query)
    
    if not docs:
        raise HTTPException(status_code=404, detail="Document Not Found")
    
    for doc in docs:
        doc.pop("_id", None)
        
    return {
        "page": page,
        "per_page": size,
        "total_results": total_count,
        "total_pages": (total_count + size - 1) // size,
        "data": docs
    }