# Python의 argparse 모듈을 사용하여 명령줄 인자를 파싱하는 기능

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", dest="info", action="store_true")


