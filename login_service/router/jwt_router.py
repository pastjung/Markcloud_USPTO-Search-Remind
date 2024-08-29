from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from core.database import get_db
from service import user_service, jwt_service

router = APIRouter(
    prefix="/api/jwt",
)

@router.post("/blacklist/delete", response_model=None)
def blacklist_delete(request: Request, response: Response, db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    
    claim = jwt_service.verify_jwt(access_token, refresh_token, db, response)
    db_user = user_service.find_user_by_user_id(claim.user_id, db)
    
    jwt_service.blacklist_delete(db_user, db)