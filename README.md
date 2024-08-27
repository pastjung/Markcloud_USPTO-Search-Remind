# MSA & DDD 디자인 패턴

> Initial written at August 27, 2024 <br/>
> last updated at: August 27, 2024


## Current: ver. 1.0.0<br/>
>* ver 1.0.0.
>   * FastAPI : Login_Service Container 추가
>   * MariaDB : User service Database 추가


# 1. 프로그램 (프로젝트) 설명

- 본 프로젝트는 MSA(마이크로서비스 아키텍처)와 DDD(도메인 주도 설계) 원칙을 따르는 방식으로 프로젝트 설계하는 방법을 공부하는 프로젝트 입니다.


# 2. Prerequisite

- 본 프로젝트는 Docker를 사용하므로 `.env.template` 파일을 참고하여 `.env` 파일에 환경 변수값을 작성해주세요.
    ```
    # 예시
    LOGIN_HOST_PORT=
    LOGIN_SERVER_PORT=
    ```
- `LOGIN_HOST_PORT`와 `login_service/entrypoint.sh` 의 포트 번호를 일치시켜주세요
    ```
    uvicorn service.main:app --host 0.0.0.0 --port 8000 --reload \
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
    ├── login-service/
    │   ├── dockerfile
    │   ├── entrypoint.sh
    │   ├── requirements.txt
    │   ├── setup.txt
    │   ├── venv/
    │   ├── service/
    │   │   ├── main.py
    │   │   ├── models/
    │   │   ├── routers/
    │   │   └── crud/
    │   └── config/
    │       ├── config.ini
    │       └── database.py
    │
    ├── .gitignore
    ├── docker-compose.yml
    ├── .env
    ├── .env.template
    └── README.md
```
