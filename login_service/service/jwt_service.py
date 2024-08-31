from fastapi import HTTPException, status, Response
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
import os
from datetime import timedelta, datetime, timezone

from schema.jwt_schema import JwtClaim
from repository import jwt_repository
from model.user_model import User, UserRole
from model.jwt_model import Blacklist

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = float(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

def create_access_token(user_id: str):
    claim={"user_id": user_id}
    claim.update({"exp": datetime.now(timezone.utc) + access_token_expires})    # timezone.utc : 세계 표준 시간 UTC로 현재 시간 설정, datetime.now() : 현재 로컬 컴퓨터의 시간 설정
    access_token = jwt.encode(claim, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def create_refresh_token():
    claim={}
    claim.update({"exp": datetime.now(timezone.utc) + refresh_token_expires})
    refresh_token = jwt.encode(claim, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token

def save_refresh_token(refresh_token: str, user_id:str, connection):
    sql = f'INSERT INTO refresh_token (token, user_id) VALUES ("{refresh_token}", "{user_id}") ON DUPLICATE KEY UPDATE token = VALUES(token)'
    jwt_repository.send_query(sql, connection, "save")

# 토큰 검증
def verify_jwt(access_token: str, refresh_token: str, connection, response: Response) -> JwtClaim:
    if is_blacklisted(access_token, connection)[0] > 0:
        raise PyJWTError("블랙리스트에 등록된 토큰입니다.")
    
    # access_token 검증
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return JwtClaim(**payload)
    except ExpiredSignatureError:       
        # access_token 만료    
        try:
            # refresh_token 검증
            sql = f'SELECT * FROM refresh_token WHERE token = "{refresh_token}"'
            result = jwt_repository.send_query(sql, connection)
            
            # 새로운 access_token 발급
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            claim={"user_id": result.user_id}
            claim.update({"exp": datetime.now(timezone.utc) + access_token_expires})
            new_access_token = jwt.encode(claim, SECRET_KEY, algorithm=ALGORITHM)

            # 쿠키 재설정 : access_token
            response.set_cookie(key="access_token", value=new_access_token, expires=access_token_expires, httponly=True)
            
            return JwtClaim(**claim)
        
        except ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Refresh Token 만료 : 다시 로그인 해주세요")
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="유효하지 않은 토큰입니다.")
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 블랙리스트 확인        
def is_blacklisted(token: str, connection):
    sql = f'SELECT COUNT(*) FROM blacklist WHERE token = "{token}"'
    result = jwt_repository.send_query(sql, connection)
    return result

# 블랙리스트 추가
def add_to_blacklist(access_token: str, refresh_token: str, connection):
    sql = f'INSERT INTO blacklist (token) VALUES ("{access_token}"), ("{refresh_token}")'
    jwt_repository.send_query(sql, connection, "save")

# 블랙리스트 비우기
def blacklist_delete(db_user: User, connection):
    if db_user.role != UserRole.admin.value:
        raise HTTPException(status_code=401, detail="Unauthorized : 관리자만 접근 가능합니다")     
    
    sql = f'DELETE FROM blacklist'
    jwt_repository.send_query(sql, connection, "save")  
    