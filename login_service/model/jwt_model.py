from sqlalchemy import Column, Integer, String, DateTime, func
from core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(512), nullable=False)
    user_id = Column(String(8), nullable=False, unique = True)

class Blacklist(Base):
    __tablename__ = "blacklist"
    
    token = Column(String(255), primary_key=True, index=True)
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())