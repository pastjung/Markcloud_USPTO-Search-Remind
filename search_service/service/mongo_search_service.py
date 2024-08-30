from typing import Optional

from schema import mongo_search_schema
from repository import mongo_search_repository


def search_by_serialNumber(serial_number : str):
    query = {"serial-number" : serial_number}
    return mongo_search_repository.search_query(query)
    
def search_by_registrationNumber(registration_number : str):
    query = {"registration-number" : registration_number}
    return mongo_search_repository.search_query(query)
    
def search_by_filingDate(start_date : str, end_date : str, page: int , size : int):
    query = {"case-file-header.filing-date": {"$gte":start_date, "$lte":end_date}}
    return mongo_search_repository.search_query_list(query, page, size)

def ordered_search_by_filingDate(
    start_date: str, 
    end_date: str, 
    page: int, 
    size: int, 
    sort_order: int
):
    query = {"case-file-header.filing-date": {"$gte": start_date, "$lte": end_date}}
    return mongo_search_repository.ordered_search_query_list(query, page, size, sort_order)


def search_by_mark_identification(workmark: str) -> Optional[mongo_search_schema.Uspto]:
    # MongoDB에서 데이터 조회
    query = {"case-file-header.mark-identification": workmark}
    result = mongo_search_repository.search_query(query)
    
    if result:
        # 데이터를 가공하여 Uspto 모델에 맞게 변환
        
        goods_service = result['case-file-statements']['case-file-statement']
        if isinstance(goods_service, list):
            goods_and_service=goods_service[0]['text']
        else:
            goods_and_service=goods_service['text']
            
        class_nums = result['classifications']['classification']
        if isinstance(class_nums, list):
            class_num = class_nums[0]['primary-code']
        else:
            class_num = class_nums['primary-code']
            
        owner = result['case-file-owners']['case-file-owner']
        if isinstance(owner, list):
            owners=owner[0]['party-name']
        else:
            owners=owner['party-name']
        
        uspto_data = mongo_search_schema.Uspto(
            workmark=result['case-file-header']['mark-identification'],
            status=result['case-file-header']['status-code'],
            goods_and_service=goods_and_service,
            class_num=class_num,
            serial=result['serial-number'],
            owners=owners,
        )
        return uspto_data
    return None