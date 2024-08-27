from pymongo import MongoClient
from starlette.config import Config

# 환경 변수 불러오기
config = Config('crawling_service/.env')
db_port = config('MONGODB_SERVER_PORT')
db_name = config('MONGODB_DB_NAME')
collection_name = config('MONGODB_COLLECTION_NAME')

client = MongoClient(f'mongodb://crawling_db:{db_port}/')
db = client[db_name]
collection = db[collection_name]