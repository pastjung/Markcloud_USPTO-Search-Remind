from pydantic import BaseModel

class Jwt(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class JwtClaim(BaseModel):
    user_id: str