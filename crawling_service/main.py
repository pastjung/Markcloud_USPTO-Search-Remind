from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from core.docs import *
from core.database import db
from router import crawling_router, search_router, move_router

def get_server():
    server = FastAPI(
        title='Crawling Service', 
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

# Fastapi 실행
app = get_server()

@app.get('/ping', tags=['Root'])
def ping():
    return 200

@app.get("/mongodb/ping", tags=['Root'])
async def mongodb_ping():
    try:
        # MongoDB에 ping 명령을 보내어 연결 확인
        db.command("ping")
        return 200
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Unable to connect to MongoDB")
    
app.include_router(crawling_router.router, tags=['Crawling'])
app.include_router(search_router.router, tags=['Search'])
app.include_router(move_router.router, tags=['Move'])