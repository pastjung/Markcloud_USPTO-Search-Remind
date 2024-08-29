from fastapi import HTTPException
from pymysql import MySQLError
from sqlalchemy import text
from sqlalchemy.orm import Session

def send_query(sql: str, session: Session, settings):
    sql = text(sql)
    try:
        result = session.execute(sql)
        
        if settings == "single":
            data = result.fetchone()    # 단일 값 추출
        elif settings == "all":
            data = result.fetchall()    # 모든 결과 추출
        elif settings == "update":
            session.commit()            # 업데이트 작업은 commit
            return None
        else:
            raise ValueError("Invalid settings value")
            
        if data is None:
            raise HTTPException(status_code=404, detail="Not Found : 데이터가 존재하지 않습니다.")
        return data
    except MySQLError as e:
        # 데이터베이스 관련 예외 처리
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except ValueError as e:
        # 잘못된 설정 값 처리
        raise HTTPException(status_code=400, detail=f"Invalid settings: {e}")
    except HTTPException as e:
        # HTTPException을 다시 발생시키는 경우, 상위 호출 스택에서 처리
        raise
    except Exception as e:
        # 일반적인 예외 처리
        raise HTTPException(status_code=500, detail="An error occurred: " + str(e))