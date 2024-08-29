from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from core.docs import *
from core.database import Base, engine
from sqlalchemy import text

def get_server():
    server = FastAPI(
        title='Signin & Signup, User Service', 
        docs_url="/docs", redoc_url=None,
        version="1.0.0",
        description=root_description,
        openapi_url="/openapi.json"
    )
    server.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    server.add_middleware(
        GZipMiddleware, minimum_size=1000
    )

    return server

# 테이블 생성
Base.metadata.create_all(bind=engine)

# Fastapi 실행
app = get_server()

@app.get('/ping', tags=['Root'])
def ping():
    return 200

@app.get("/mariadb/ping", tags=['Root'])
async def mariadb_ping():
    try:
        # 데이터베이스 연결 테스트
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return 200
            else:
                raise HTTPException(status_code=500, detail="Unexpected result from database")
    except Exception as e:
        # 연결 오류 발생 시
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")