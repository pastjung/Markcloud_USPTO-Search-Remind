# 설정 파일에서 가져온 시간 제한, 재시도 값을 사용해 HTTP GET 요청을 처리, 실패할 경우 계속 재시도

import time
import requests
from functools import wraps
from utils import (
    logger,
    properties
)

class ProxyRequest(requests.Session):

    @classmethod
    def get(cls,        # cls : 해당 메서드를 호출한 클래스 자체를 가리킴 -> 여기서 ProxyRequest.get() 형태로 클래스 자체에서 호출시 cls 는 ProxyRequest 클래스 자체를 가리킴
            url,
            timeout=int(properties['GET']['ITEM_TIMEOUT']),
            delay=int(properties['DELAY']['FACTOR']),
            *args,
            **kwargs
    ):
        counter = 0
        session = cls()
        while True:
            try:
                response = super(ProxyRequest, session).get(url=url,
                                                            timeout=timeout,
                                                            *args,
                                                            **kwargs)
                return response


            except requests.exceptions.Timeout as TO:
                counter += 1
                timeout += delay

                if counter % 10 == 0:
                    time.sleep(timeout)

                if counter == 30:
                    raise TO

            except Exception as e:
                raise e

# 예외 발생시 repeater 를 사용하여 로깅하고 재시도
def repeater(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        while True:
            try:
                return await f(*args, **kwargs)
            except Exception as e:
                logger.error(f'{e}', exc_info=True)
    return wrapper