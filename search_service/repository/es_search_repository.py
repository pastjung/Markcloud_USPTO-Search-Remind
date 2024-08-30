from core.database import es, ELASTICSEARCH_INDEX

def search_query(query: dict):
    response = es.search(index=ELASTICSEARCH_INDEX, body=query)
    return response