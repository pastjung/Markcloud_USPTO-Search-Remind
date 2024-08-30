# (주) 마크클라우드 인턴 기간 작업 내용 리마인드

> Initial written at August 27, 2024 <br/>
> last updated at: August 28, 2024


## Current: ver. 1.0.1<br/>
>* ver 1.0.0.
>   * Python  : Crawling_Service
>   * FastAPI : Login_Service, Search_Service_Container 추가
>   * MariaDB : User service Database 추가
>   * MongoDB : Crawling Service Database 추가
>   * Elasticsearch : 검색 엔진 Database 추가 ( 레플리카 설정 추가 → 클러스터 상태 = GREEN )
>   * Kibana : 모니터링 시스템 추가

>* ver 1.0.1.
>    * Crawling_Service : Python -> FastAPI
>    * Architecture : MSA -> MSA + DDD + Clean
>    * 코드 최적화 + 프로젝트 통합

# 1. 프로그램 (프로젝트) 설명

- 본 프로젝트는 (주) 마크클라우드 인턴 기간 2024.07.22 ~ 2024.08.16 동안 수행한 작업을 리마인드하는 프로젝트 입니다
- 본 프로젝트는 Linux OS 환경을 기반으로 동작하도록 설계 되었습니다
- 본 프로젝트의 데이터 크롤링 URL의 경우 비공개 정보입니다
    - 정보 권한이 있는 분들은 [링크](https://github.com/pastjung/Markcloud_USPTO-Search)를 통해 URL 정보를 포함한 .env 파일을 확인해 주세요
- 본 프로젝트의 기능은 아래와 같습니다
    - FastAPI와 MariaDB 를 사용해 로그인/회원가입 및 사용자 기능을 수행하며 이때 쿠키를 사용합니다
    - USPTO 데이터를 크롤링하여 MongoDB에 데이터를 저장합니다
    - 이때 비동기 및 멀티쓰레드 방식으로 다운로드, 멀티프로세싱 방식으로 압축해제 작업을 수행하여 성능을 향상시켰습니다
    - MongoDB에 저장된 데이터를 Elasticsearch에 옮겨 검색을 하여 검색 성능을 향상시켰습니다
    - Kibana를 통해 Elasticsearch에 저장된 데이터를 효과적으로 관리했습니다
    - Elasticsearch 노드의 레플리카를 설정하여 클러스터 상태를 GREEN 상태로 변경했습니다
    - Elasticsearch 분석기를 사용해 약어, 오타, 대소문자 구분 등의 처리를 하여 검색 성능을 향상시켰습니다.
- 본 프로젝트는 MSA 및 DDD 방식으로 프로젝트를 구상했습니다


# 2. Prerequisite

- 본 프로젝트는 Docker를 사용하므로 `.env.template` 파일을 참고하여 `.env` 파일에 환경 변수값을 작성해주세요.
    ```
    # 예시
    LOGIN_HOST_PORT=
    LOGIN_SERVER_PORT=

    MARIADB_ID=
    MARIADB_ROOT_PASSWORD=
    MARIADB_DB_NAME=

    MARIADB_HOST_PORT=
    MARIADB_SERVER_PORT=

    CRAWLING_HOST_PORT=
    CRAWLING_SERVER_PORT=

    MONGODB_HOST_PORT=
    MONGODB_SERVER_PORT=

    MONGODB_DB_NAME=
    MONGODB_COLLECTION_NAME=

    SEARCH_HOST_PORT=
    SEARCH_SERVER_PORT=

    ELASTIC_PASSWORD=
    ELASTICSEARCH_INDEX=

    KIBANA_HOST_PORT=
    KIBANA_SERVER_PORT=

    SECRET_KEY=
    ALGORITHM=
    ACCESS_TOKEN_EXPIRE_MINUTES=
    REFRESH_TOKEN_EXPIRE_DAYS=

    URL=
    ```
- `LOGIN_SERVER_PORT`와 `login_service/entrypoint.sh` 의 포트 번호를 일치시켜주세요
    ```
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload \
    ```
- `CRAWLING_SERVER_PORT`와 `crawling_service/entrypoint.sh` 의 포트 번호를 일치시켜주세요
    ```
    uvicorn main:app --host 0.0.0.0 --port 8001 --reload \
    ```
- `SEARCH_SERVER_PORT`와 `search_service/entrypoint.sh` 의 포트 번호를 일치시켜주세요
    ```
    uvicorn main:app --host 0.0.0.0 --port 8002 --reload \
    ```

# 3. 구동 방법

## 3.1. 프로젝트 실행

본 프로젝트는 Docker Compose를 사용하므로 이를 실행시켜주세요.

```shell
(sudo) docker compose up (--build)
```

# 4. 디렉토리 및 파일 설명
```
    /project-root
    │
    ├── crawling_service/
    │   ├── dockerfile
    │   ├── entrypoint.sh
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── setup.txt
    │   ├── venv/
    │   ├── core/
    │   │   ├── config.ini
    │   │   ├── docs.py
    │   │   └── database.py
    │   ├── model/
    │   │   ├── ContentsHandler.py
    │   │   ├── DatabaseManager.py
    │   │   ├── DownloadManager.py
    │   │   └── parser_model.py
    │   ├── router/
    │   │   ├── crawling_router.py
    │   │   └── move_router.py
    │   ├── service/
    │   │   ├── crawling_service.py
    │   │   └── move_service.py
    │   └── utils/
    │       ├── __init__.py
    │       ├── arguments.py
    │       ├── configs.py
    │       ├── logs.py
    │       └── proxies.py
    │
    ├── login_service/
    │   ├── dockerfile
    │   ├── entrypoint.sh
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── setup.txt
    │   ├── venv/
    │   ├── core/
    │   │   ├── config.ini
    │   │   ├── docs.py
    │   │   └── database.py
    │   ├── model/
    │   │   ├── jwt_model.py
    │   │   └── user_model.py
    │   ├── repository/
    │   │   ├── jwt_repository.py
    │   │   └── user_repository.py
    │   ├── router/
    │   │   ├── jwt_router.py
    │   │   └── user_router.py
    │   ├── schema/
    │   │   ├── jwt_schema.py
    │   │   └── user_schema.py
    │   └── service/
    │       ├── jwt_service.py
    │       └── user_service.py
    │
    ├── search_service/
    │   ├── dockerfile
    │   ├── entrypoint.sh
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── setup.txt
    │   ├── venv/
    │   ├── core/
    │   │   ├── docs.py
    │   │   └── database.py
    │   ├── repository/
    │   │   ├── es_search_repository.py
    │   │   └── mongo_search_repository.py
    │   ├── router/
    │   │   ├── es_search_router.py
    │   │   └── mongo_search_router.py
    │   ├── schema/
    │   │   └── mongo_search_schema.py
    │   └── service/
    │       ├── es_search_service.py
    │       └── mongo_search_service.py
    │
    ├── .env
    ├── .env.template
    ├── .gitignore
    ├── docker-compose.yml
    └── README.md
```
