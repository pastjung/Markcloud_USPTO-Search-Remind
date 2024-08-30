from elasticsearch import helpers
from fastapi import HTTPException
from elasticsearch.helpers import BulkIndexError

from core.database import collection, es, ELASTICSEARCH_INDEX

def move_to_elasticsearch():
    # MongoDB에서 데이터 읽기
    documents = collection.find()
    
    actions = (transform_data(doc) for doc in documents)

    # 인덱스 생성
    create_index()
    
    # Elasticsearch로 데이터 전송
    try:
        helpers.bulk(es, actions, chunk_size=5)    # chunk_size 를 통해 한번에 전송하는 데이터 크기 조절
    except BulkIndexError as e:
        error_details = []
        for error in e.errors:
            # 오류 정보 추출
            document_id = error.get('_id', 'unknown_id')
            error_info = error.get('index', {}).get('error', {})
            error_reason = error_info.get('reason', 'No reason provided')
            error_details.append({
                'id': document_id,
                'error': error_reason
            })
            
        raise HTTPException(
            status_code=500,
            detail={
                'message': 'One or more documents failed to index.',
                'errors': error_details
            })

# 인덱스 설정과 매핑 : edge_ngram 을 사용해 Custom Analyzer 를 만들어 약어 또한 검색 가능하도록 설계
def create_index():
    index_settings = {
        "settings": {
            "number_of_shards": 2,  # 샤드 수를 5로 설정
            "number_of_replicas": 1,  # 각 샤드의 복제본을 1개로 설정
            "analysis": {
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20,
                        "token_chars": ["letter", "digit"]
                    }
                },
                "analyzer": {
                    "edge_ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "edge_ngram_tokenizer",
                        "filter": ["lowercase"]
                    },
                    "standard_analyzer": {
                        "type": "standard",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    "type": "keyword"  # 'id'는 unique identifier로 사용되므로 'keyword'
                },
                "serial-number": {
                    "type": "keyword"  # 고유값으로 사용되는 필드
                },
                "us-code": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "registration-number": {
                    "type": "text"
                },
                "filing-date": {
                    # "type": "date",
                    # "format": "yyyyMMdd"
                    "type": "text"
                },
                "goods_and_service": {
                    "type": "text",
                    "analyzer": "standard_analyzer"
                },
                "owners": {
                    "type": "text",
                    "analyzer": "standard_analyzer"
                },
                "workmark": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"  # 약어 검색을 위해 edge_ngram_analyzer 사용
                },
                "workmark_abbr": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"  # 약어 검색을 위해 edge_ngram_analyzer 사용
                },
                "status": {
                    "type": "text",
                    "analyzer": "standard_analyzer"
                },
                "class_num": {
                    "type": "text",
                    "analyzer": "standard_analyzer"
                }
            }
        }
    }
    
    # 인덱스 생성 요청
    es.indices.create(index=ELASTICSEARCH_INDEX, body=index_settings, ignore=400)
        
def transform_data(doc):
    # MongoDB 문서를 Elasticsearch 문서로 변환   
    
    case_file_statements = doc.get('case-file-statements', {}).get('case-file-statement', [])
    if isinstance(case_file_statements, dict):
        goods_and_service = case_file_statements.get('text', '')
    elif isinstance(case_file_statements, list) and len(case_file_statements) > 0:
        goods_and_service = case_file_statements[0].get('text', '')
    else:
        goods_and_service = ''
    
    case_file_owners = doc.get('case-file-owners', {}).get('case-file-owner', {})
    if isinstance(case_file_owners, dict):
        owners = case_file_owners.get('party-name', '')
    elif isinstance(case_file_owners, list) and len(case_file_owners) > 0:
        owners = case_file_owners[0].get('party-name', '')
        
    classifications = doc.get('classifications', {}).get('classification', {})
    if isinstance(classifications, dict):
        class_num = classifications.get('primary-code', '')
        us_code = classifications.get('us-code', [])
    elif isinstance(classifications, list) and len(classifications) > 0:
        class_num = classifications[0].get('primary-code', '')
        us_code = classifications[0].get('us-code', [])
    
    if isinstance(us_code, str):
        us_code = [us_code]
        
    workmark = doc.get('case-file-header', {}).get('mark-identification', '')
    workmark_abbr = generate_abbr(workmark)
    
    return {
        "_index": ELASTICSEARCH_INDEX,
        "_id": str(doc['_id']),
        "_source": {
            "id": str(doc['_id']),
            "serial-number": doc.get('serial-number', ''),
            "us-code": us_code,    # 배열 형태로 저장
            "registration-number": doc.get('registration-number', ''),
            "filing-date": doc.get('case-file-header', {}).get('filing-date', ''),
            "goods_and_service": goods_and_service,
            "owners": owners,
            "workmark": workmark,
            "workmark_abbr": workmark_abbr,  # 약어 추가
            "status": doc.get('case-file-header', {}).get('status-code', ''),
            "class_num": class_num
        }
    }
    
def generate_abbr(text):
    """
    입력된 텍스트에서 약어를 생성합니다.
    예를 들어, 'Personal Computer' -> 'PC'
    """
    words = text.split()
    abbr = ''.join(word[0].upper() for word in words if len(word) > 1)  # 두 글자 이상의 단어의 첫 글자를 대문자로
    return abbr