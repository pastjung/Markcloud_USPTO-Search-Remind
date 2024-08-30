from model.parser_model import PathTreeParser
from model.DatabaseManager import DatabaseManager
from model.ContentsHandler import ContentsHandler

def get_latest():
    handler = ContentsHandler(PathTreeParser)
    db_manager = DatabaseManager()
    
    handler.get_last().decompress().clean_up()      # 크롤링후 압축해제
    db_manager.input_files()                        # MongoDB에 저장
    db_manager.clean_up()

def get_all():
    handler = ContentsHandler(PathTreeParser)
    db_manager = DatabaseManager()
    
    handler.get_all().decompress().clean_up()
    db_manager.input_files()
    db_manager.clean_up()