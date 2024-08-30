# Python의 cinfigparser 모듈을 사용하여 설정 파일을 읽어오기

from configparser import ConfigParser
properties = ConfigParser()
properties.read('core/config.ini')