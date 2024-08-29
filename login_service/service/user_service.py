from fastapi import HTTPException
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from schema.user_schema import UserSignup, UserSignin, UserInfo
from model.user_model import User, UserRole
from repository import user_repository
from service import jwt_service
from service.jwt_service import access_token_expires

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def user_signup(user:UserSignup, connection):
    # ID 체크
    verify_user_id(user.user_id, connection)
    
    # 계정 생성
    sql = f'INSERT INTO user (user_id, nickname, password, birth, role) VALUES ("{user.user_id}", "{user.nickname}", "{pwd.hash(user.password)}", "{user.birth}", "{UserRole.user.value}")'
    user_repository.send_query(sql, connection, "update")
    
def user_signin(user:UserSignin, connection):
    db_user = find_user_by_user_id(user.user_id, connection)
    
    # 비밀번호 검증
    verify_password(user.password, db_user.password)
    
    # JWT 생성
    access_token = jwt_service.create_access_token(db_user.user_id)
    refresh_token = jwt_service.create_refresh_token(db_user.user_id)
    jwt_service.save_refresh_token(refresh_token, db_user.user_id, connection)
    
    return access_token, access_token_expires
    
def user_logout(access_token: str, connection):
    jwt_service.add_to_blacklist(access_token, connection)
    
def user_read(access_token: str, connection) -> User:
    claim = jwt_service.verify_jwt(access_token, connection)
    return find_user_by_user_id(claim.user_id, connection)
    
def user_read_all(access_token: str, connection) -> list[User]:
    claim = jwt_service.verify_jwt(access_token, connection)
    db_user = find_user_by_user_id(claim.user_id, connection)
    
    if db_user.role != UserRole.admin.value:
        raise HTTPException(status_code=401, detail="Unauthorized : 관리자만 접근 가능합니다")
    
    sql = f'SELECT * FROM user'
    return user_repository.send_query(sql, connection, "all")
    
def user_update(access_token: str, user_update:UserSignup, connection):
    claim = jwt_service.verify_jwt(access_token, connection)
    db_user = find_user_by_user_id(claim.user_id, connection)
    
    if claim.user_id != user_update.user_id:
        verify_user_id(user_update.user_id, connection)
        
    sql = f'UPDATE user SET user_id = "{user_update.user_id}", nickname = "{user_update.nickname}", password = "{pwd.hash(user_update.password)}", birth = "{user_update.birth}" WHERE id = "{db_user.id}"'
    user_repository.send_query(sql, connection, "update")
    
    jwt_service.add_to_blacklist(access_token, connection)
    
def user_delete(access_token: str, connection):
    claim = jwt_service.verify_jwt(access_token, connection)
    db_user = find_user_by_user_id(claim.user_id, connection)
    
    sql = f'DELETE FROM user WHERE id = "{db_user.id}"'
    user_repository.send_query(sql, connection, "update")
    
    jwt_service.add_to_blacklist(access_token, connection)
    
def user_role_admin(access_token:str, connection):
    claim = jwt_service.verify_jwt(access_token, connection)
    db_user = find_user_by_user_id(claim.user_id, connection)
    
    if(db_user.role == UserRole.admin.value):
        raise HTTPException(status_code=400, detail="이미 관리자입니다.")
    
    sql = f'UPDATE user SET role = "{UserRole.admin.value}" where id = "{db_user.id}"'
    user_repository.send_query(sql, connection, "update")
    
def user_role_user(access_token:str, connection):
    claim = jwt_service.verify_jwt(access_token, connection)
    db_user = find_user_by_user_id(claim.user_id, connection)
    
    if(db_user.role == UserRole.user.value):
        raise HTTPException(status_code=400, detail="이미 사용자입니다.")
    
    sql = f'UPDATE user SET role = "{UserRole.user.value}" where id = "{db_user.id}"'
    user_repository.send_query(sql, connection, "update")
    

# DB에 user_id이 존재하는지 확인
def verify_user_id(user_id: str, connection):
    sql = f'SELECT COUNT(*) as count FROM user WHERE user_id = "{user_id}"'
    result = user_repository.send_query(sql, connection, "single")
    
    if result[0] > 0:
        raise HTTPException(status_code=409, detail="이미 존재하는 사용자 이름입니다.")

# 입력된 비밀번호가 암호화된 비밀번호와 일치하는지 검증
def verify_password(password: str, hashed_password: str):
    try:
         # 암호 검증 로직
        if not pwd.verify(password, hashed_password):
            raise HTTPException(status_code=400, detail="Invalid password")
    except UnknownHashError as e:
        # 해시가 인식되지 않을 때 발생하는 예외 처리
        raise HTTPException(status_code=400, detail="Invalid password")
    except ValueError as e:
        # 암호화 관련 예외 처리
        raise HTTPException(status_code=400, detail="Password verification error: " + str(e))
    except HTTPException as e:
        # HTTPException을 다시 발생시키는 경우, 상위 호출 스택에서 처리
        raise
    except Exception as e:
        # 일반적인 예외 처리
        raise HTTPException(status_code=500, detail="An error occurred during password verification: " + str(e))
    
# user_id를 사용해 User 검색
def find_user_by_user_id(user_id: str, connection) -> User:
    sql = f'SELECT * FROM user WHERE user_id = "{user_id}"'
    result = user_repository.send_query(sql, connection, "single")
    return result