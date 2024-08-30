from abc import (
    ABCMeta,
    abstractmethod
)
from lxml import html

class ParserInterface(metaclass=ABCMeta):   # 추상 클래스 : 파싱 인터페이스
    
    @abstractmethod
    def parse(cls, response): 
        raise NotImplementedError


class PathTreeParser(ParserInterface):      # ParserInterface 상속
    
    @classmethod
    def parse(cls, response):                       # 추상 클래스 함수 구현
        tree = html.fromstring(response.content)    # response 내용을 HTML 트리로 파싱
        item_links = tree.xpath('//td/a/text()')    # xpath 를 사용해 HTML 트리에서 모든 <td> 아래 <a> 태그의 링크 텍스트 추출
        return item_links                           # 추출한 링크 반환