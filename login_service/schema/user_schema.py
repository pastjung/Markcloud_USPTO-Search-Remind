from pydantic import BaseModel, field_validator
from model.user_model import UserRole

class UserResponse(BaseModel):
    id : int
    user_id: str
    nickname: str
    birth: str
    role: UserRole

class UserSignup(BaseModel):
    user_id: str
    nickname: str
    password: str
    birth: str  | None = None

    @field_validator('user_id', 'password', 'nickname')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
class UserSignin(BaseModel):
    user_id : str
    password : str
        
class UserInfo(BaseModel):
    user_id : str
    nickname : str
    birth : str | None = None
    
