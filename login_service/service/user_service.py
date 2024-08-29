from fastapi import HTTPException
from passlib.context import CryptContext

from schema.user_schema import UserSignup, UserSignin, UserInfo
from model.user_model import User, UserRole
from repository.user_repository import send_query

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def user_signup(user:UserSignup, connection):
    # ID 체크
    verify_user_id(user.user_id, connection)
    
    # 계정 생성
    sql = f'INSERT INTO user (user_id, nickname, password, birth, role) VALUES ("{user.user_id}", "{user.nickname}", "{pwd.hash(user.password)}", "{user.birth}", "{UserRole.user.value}")'
    send_query(sql, connection, "update")
    
def user_signin(user:UserSignin, connection):
    None
    
def user_logout(user:UserInfo, connection):
    None    
    
def user_read(user:UserInfo, connection) -> User:
    sql = f'SELECT * FROM user WHERE user_id = "{user.user_id}"'
    result = send_query(sql, connection, "single")
    return result
    
def user_read_all(user:UserInfo, connection) -> list[User]:
    db_user = user_read(user, connection)
    
    if db_user.role != UserRole.admin.value:
        raise HTTPException(status_code=401, detail="Unauthorized : 관리자만 접근 가능합니다")
    
    sql = f'SELECT * FROM user'
    return send_query(sql, connection, "all")
    
def user_update(user:UserInfo, user_update:UserSignup, connection):
    db_user = user_read(user, connection)
    
    if user.user_id != user_update.user_id:
        verify_user_id(user_update.user_id, connection)
        
    sql = f'UPDATE user SET user_id = "{user_update.user_id}", nickname = "{user_update.nickname}", password = "{pwd.hash(user_update.password)}", birth = "{user_update.birth}" WHERE id = "{db_user.id}"'
    send_query(sql, connection, "update")
    
def user_delete(user:UserInfo, connection):
    db_user = user_read(user, connection)
    
    sql = f'DELETE FROM user WHERE id = "{db_user.id}"'
    send_query(sql, connection, "update")
    
def user_role_admin(user:UserInfo, connection):
    db_user = user_read(user, connection)
    
    if(db_user.role == UserRole.admin.value):
        raise HTTPException(status_code=400, detail="이미 관리자입니다.")
    
    sql = f'UPDATE user SET role = "{UserRole.admin.value}" where id = "{db_user.id}"'
    send_query(sql, connection, "update")
    
def user_role_user(user:UserInfo, connection):
    db_user = user_read(user, connection)
    
    if(db_user.role == UserRole.user.value):
        raise HTTPException(status_code=400, detail="이미 사용자입니다.")
    
    sql = f'UPDATE user SET role = "{UserRole.user.value}" where id = "{db_user.id}"'
    send_query(sql, connection, "update")
    

# DB에 user_id이 존재하는지 확인
def verify_user_id(user_id: str, connection):
    sql = f'SELECT COUNT(*) as count FROM user WHERE user_id = "{user_id}"'
    result = send_query(sql, connection, "single")
    
    if result[0] > 0:
        raise HTTPException(status_code=409, detail="이미 존재하는 사용자 이름입니다.")