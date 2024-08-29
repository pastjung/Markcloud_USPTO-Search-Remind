from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from core.database import get_db
from schema import user_schema
from service import user_service, jwt_service

router = APIRouter(
    prefix="/api/user",
)

@router.post("/signup", response_model=None)
def user_signup(user:user_schema.UserSignup, db:Session=Depends(get_db)):
    user_service.user_signup(user, db)
    
@router.post("/signin", response_model=None)
def user_signin(response: Response, user:user_schema.UserSignin, db:Session=Depends(get_db)):
    user_service.user_signin(user, db, response)
    
@router.post("/logout", response_model=None)
def user_logout(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_service.user_logout(access_token, refresh_token, db, response)
    
@router.get("/read", response_model=user_schema.UserResponse)
def user_read(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    return user_service.user_read(access_token, refresh_token, db, response)

@router.get("/read/all", response_model=list[user_schema.UserResponse])
def user_read_all(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    return user_service.user_read_all(access_token, refresh_token, db, response)
    
@router.post("/update", response_model=None)
def user_update(request: Request, response: Response, user_update:user_schema.UserSignup, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_service.user_update(access_token, refresh_token, user_update, db, response)
    
@router.post("/delete", response_model=None)
def user_delete(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_service.user_delete(access_token, refresh_token, db, response)
    
@router.post("/role-admin", response_model=None)
def user_role_admin(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_service.user_role_admin(access_token, refresh_token, db, response)
        
@router.post("/role-user", response_model=None)
def user_role_user(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_service.user_role_user(access_token, refresh_token, db, response)