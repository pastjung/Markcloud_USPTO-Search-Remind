'''
* sqlalchemy 와 같은 ORM 을 사용해 데이터베이스와 상호작용하기 위한 모델 정의
* API의 요청 및 응답 데이터의 직렬화 및 역직렬화를 schema 를 통해 수행하도록 설계 -> 민감 정보 노출 방지
'''

from sqlalchemy import Column, Integer, String, Enum
from core.database import Base
from enum import Enum as PyEnum

class UserRole(PyEnum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(15), nullable=False)    # 아이디
    nickname = Column(String(15), nullable=False)   # 이름
    password = Column(String(100), nullable=False)  # 비밀번호
    role = Column(Enum(UserRole), nullable=False)   # 권한
    birth = Column(String(8), nullable=True)        # 생년월일 