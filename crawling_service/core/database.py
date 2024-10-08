from pymongo import MongoClient
import os
from elasticsearch import Elasticsearch

# MongoDB : 환경 변수 불러오기
db_port = os.getenv('MONGODB_SERVER_PORT')
db_name = os.getenv('MONGODB_DB_NAME')
collection_name = os.getenv('MONGODB_COLLECTION_NAME')

client = MongoClient(f'mongodb://crawling_db:{db_port}/')
db = client[db_name]
collection = db[collection_name]

# Elasticsearch : 환경 변수 불러오기
ELASTICSEARCH_SERVER_PORT = os.getenv("ELASTICSEARCH_SERVER_PORT")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")

ELASTICSEARCH_URL = f"http://es01:{ELASTICSEARCH_SERVER_PORT}"
es = Elasticsearch(ELASTICSEARCH_URL)