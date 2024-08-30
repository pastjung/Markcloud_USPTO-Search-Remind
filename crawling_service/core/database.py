from pymongo import MongoClient
import os

# 환경 변수 불러오기
db_port = os.getenv('MONGODB_SERVER_PORT')
db_name = os.getenv('MONGODB_DB_NAME')
collection_name = os.getenv('MONGODB_COLLECTION_NAME')

client = MongoClient(f'mongodb://crawling_db:{db_port}/')
db = client[db_name]
collection = db[collection_name]