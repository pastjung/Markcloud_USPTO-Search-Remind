from repository import es_search_repository

def find_data_from_elasticsearch(workmark, sort_method, sort_order, size=500, max_results=11000):
    """
    Elasticsearch에서 데이터를 검색하는 함수입니다.
    
    :param workmark: 검색할 workmark 값
    :param sort_method: 정렬할 필드 ( 1: serial-number, 2: us-code.keyword, 3: _id )
    :param sort_order: 정렬 방향 ( 1: 오름차순, -1: 내림차순 )
    :param size: 한 번에 조회할 행의 수
    :param max_results: 최대 결과 수
    :return: 결과 리스트
    """
    all_results = []
    last_sort_value = None
    
    if sort_method == 1:
        sort_field = "serial-number"
    elif sort_method == 2:
        sort_field = "us-code.keyword"
    else: 
        sort_field = "_id"
    
    while len(all_results) < max_results:
        # 쿼리 정의
        query = {
            "size": size,           # 한 번에 조회할 행의 수
            "sort": [               # 정렬 기준
                { sort_field: "asc" if sort_order == 1 else "desc" }
            ],
            "query": {              # 조회 조건
                "bool": {
                    "should": [
                        {
                            "match": {
                                "workmark": {
                                    "query": workmark,
                                    "fuzziness": "1",
                                    "operator": "and",   # must의 operator 기본 값 : or (입력값의 모든 단어중 포함하는 단어가 있을 경우 통과)
                                }
                            }
                        }
                    ],
                    "minimum_should_match": 1  # 하나 이상의 should 조건이 만족해야 함
                }
            }
        }
        
        if len(workmark) > 1:
            # 약어 검색을 추가
            query["query"]["bool"]["should"].append({
                "match": {
                    "workmark_abbr": {
                        "query": workmark,
                        "operator": "and"  # 모든 단어가 포함된 문서
                    }
                }
            })

        # search_after를 사용하여 이전 페이지의 마지막 문서 기준으로 검색
        if last_sort_value:
            query["search_after"] = [last_sort_value]
        
        # Elasticsearch에서 검색
        response = es_search_repository.search_query(query)
        
        # 결과 가공
        hits = response["hits"]["hits"]
        if not hits:
            break  # 더 이상 결과가 없으면 종료
        
        all_results.extend([hit["_source"] for hit in hits])
        
        # 마지막 문서의 정렬 필드 값을 추출하여 search_after에 사용
        last_sort_value = hits[-1]["sort"][0]

    return {"results": all_results}    

def find_all_data_from_elasticsearch(sort_method, sort_order, size=500, max_results=11000):
    """
    Elasticsearch에서 모든 데이터를 페이지네이션으로 가져오는 함수입니다.
    
    :param sort_method: 정렬할 필드 ( 1: serial-number, 2: us-code.keyword, 3: _id )
    :param sort_order: 정렬 방향 ( 1: 오름차순, -1: 내림차순 )
    :param size: 한 번에 조회할 행의 수
    :param max_results: 최대 결과 수
    :return: 결과 리스트
    """
    
    all_results = []
    last_sort_value = None    
    
    if sort_method == 1:
        sort_field = "serial-number"
    elif sort_method == 2:
        sort_field = "us-code.keyword"
    else: 
        sort_field = "_id"
    
    while len(all_results) < max_results:
        # 쿼리 정의
        query = {
            "size": size,  # 한 번에 조회할 행의 수
            "sort": [
                { sort_field: "asc" if sort_order == 1 else "desc" }
            ],
            "query": {
                "match_all": {}  # 모든 데이터를 가져오는 쿼리
            }
        }

        # search_after를 사용하여 이전 페이지의 마지막 문서 기준으로 검색
        if last_sort_value:
            query["search_after"] = [last_sort_value]

        # Elasticsearch에서 검색
        response = es_search_repository.search_query(query)

        # 결과 가공
        hits = response["hits"]["hits"]
        if not hits:
            break  # 더 이상 결과가 없으면 종료

        all_results.extend([hit["_source"] for hit in hits])

        # 마지막 문서의 정렬 필드 값을 추출하여 search_after에 사용
        last_sort_value = hits[-1]["sort"][0]

    return {"results": all_results}