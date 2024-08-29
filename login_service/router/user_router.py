from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schema import user_schema
from service import user_service

router = APIRouter(
    prefix="/api/user",
)

@router.post("/signup", response_model=None)
def user_signup(user:user_schema.UserSignup, db:Session=Depends(get_db)):
    user_service.user_signup(user, db)
    
@router.post("/signin", response_model=None)
def user_signin(user:user_schema.UserSignin, db:Session=Depends(get_db)):
    user_service.user_signin(user, db)
    
@router.post("/logout", response_model=None)
def user_logout(user:user_schema.UserInfo, db:Session=Depends(get_db)):
    user_service.user_logout(user, db)
    
@router.post("/read", response_model=user_schema.UserResponse)
def user_read(user:user_schema.UserInfo, db:Session=Depends(get_db)):
    return user_service.user_read(user, db)

@router.post("/read/all", response_model=list[user_schema.UserResponse])
def user_read_all(user:user_schema.UserInfo, db:Session=Depends(get_db)):
    return user_service.user_read_all(user, db)
    
@router.post("/update", response_model=None)
def user_update(user:user_schema.UserInfo, user_update:user_schema.UserSignup, db:Session=Depends(get_db)):
    user_service.user_update(user, user_update, db)
    
@router.post("/delete", response_model=None)
def user_delete(user:user_schema.UserInfo, db:Session=Depends(get_db)):
    user_service.user_delete(user, db)
    
@router.post("/role-admin", response_model=None)
def user_role_admin(user:user_schema.UserInfo, db:Session=Depends(get_db)):
    user_service.user_role_admin(user, db)
    
@router.post("/role-user", response_model=None)
def user_role_user(user:user_schema.UserInfo, db:Session=Depends(get_db)):
    user_service.user_role_user(user, db)    